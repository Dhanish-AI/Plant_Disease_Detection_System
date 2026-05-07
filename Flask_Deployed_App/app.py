from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from werkzeug.utils import secure_filename
from models import db, User, DiseaseHistory, Notification, Feedback
from werkzeug.security import generate_password_hash, check_password_hash

# Load your data and model
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

# Add plant care information with disease-specific details
disease_info['growing_tips'] = [
    # Apple diseases (0-3)
    "Maintain proper tree spacing and prune regularly for good air circulation. Remove infected leaves.",
    "Water at base, avoid overhead watering. Mulch to maintain soil moisture.",
    "Plant resistant varieties. Ensure good drainage and full sun exposure.",
    "Regular pruning to improve air flow. Remove any infected fruit and leaves.",
    
    # Blueberry diseases (4-7)
    "Deep, low pH mulch like peat moss or pine needles. Water during day, keep soil moist not soggy.",
    "Plant in well-draining acidic soil. Maintain proper spacing between plants.",
    "Provide good air circulation. Remove infected plant parts promptly.",
    "Mulch with organic materials. Avoid overhead irrigation.",
    
    # Cherry diseases (8-11)
    "Plant in full sun with good air movement. Space trees properly.",
    "Prune to maintain open canopy. Remove fallen leaves and fruit.",
    "Ensure proper soil drainage. Avoid waterlogged conditions.",
    "Regular monitoring and pruning of affected branches.",
    
    # Corn diseases (12-15)
    "Plant in well-drained soil. Rotate crops annually.",
    "Maintain proper plant spacing. Control weeds effectively.",
    "Use disease-resistant varieties. Time planting to avoid stress periods.",
    "Proper fertilization and irrigation management.",
    
    # Grape diseases (16-19)
    "Train vines for good air circulation. Remove excess foliage.",
    "Use trellis systems. Maintain proper vine spacing.",
    "Prune during dormancy. Remove infected materials.",
    "Apply fungicides preventively in humid conditions.",
    
    # Peach diseases (20-23)
    "Annual pruning for open canopy. Remove dead wood.",
    "Proper spacing between trees. Avoid overhead irrigation.",
    "Plant resistant varieties. Monitor regularly for signs.",
    "Maintain good orchard sanitation.",
    
    # Pepper diseases (24-27)
    "Plant in warm, well-drained soil. Avoid overcrowding.",
    "Stake plants for better air circulation.",
    "Rotate crops. Avoid working with wet plants.",
    "Use mulch to prevent soil splash.",
    
    # Potato diseases (28-31)
    "Plant certified seed potatoes. Rotate crops.",
    "Hill soil around plants. Maintain consistent moisture.",
    "Space plants properly. Remove infected plants.",
    "Store tubers in cool, dry conditions.",
    
    # Strawberry diseases (32-35)
    "Plant in raised beds with good drainage.",
    "Use mulch to keep fruit off soil.",
    "Remove runners to improve air circulation.",
    "Avoid overhead watering.",
    
    # Tomato diseases (36-38)
    "Stake or cage plants for better air flow.",
    "Mulch soil and water at base of plants.",
    "Remove lower leaves touching soil."
]

disease_info['benefits'] = [
    # Apple benefits (0-3)
    "Rich in antioxidants and fiber. Helps regulate blood sugar.",
    "Contains quercetin for brain health. Supports heart function.",
    "High in vitamin C and potassium. Aids digestion.",
    "Good source of pectin. Promotes gut health.",
    
    # Blueberry benefits (4-7)
    "Low in calories, high in nutrients. King of antioxidants.",
    "Protects against aging and DNA damage. Reduces cancer risk.",
    "Lowers blood pressure. Supports heart health.",
    "Improves memory and brain function. Anti-inflammatory.",
    
    # Cherry benefits (8-11)
    "Rich in anthocyanins. Natural sleep aid with melatonin.",
    "Reduces inflammation. Supports muscle recovery.",
    "High in antioxidants. Helps with arthritis pain.",
    "Supports healthy skin. Boosts immune system.",
    
    # Corn benefits (12-15)
    "Good source of fiber. Supports digestive health.",
    "Rich in B vitamins. Boosts energy levels.",
    "Contains antioxidants. Promotes eye health.",
    "High in essential minerals. Supports bone health.",
    
    # Grape benefits (16-19)
    "High in resveratrol. Promotes longevity.",
    "Rich in antioxidants. Supports skin health.",
    "Good source of vitamins K and C. Strengthens bones.",
    "Contains polyphenols. Heart health benefits.",
    
    # Peach benefits (20-23)
    "Low calorie, nutrient dense. Good for weight management.",
    "Rich in vitamin C. Supports immune system.",
    "Contains beta carotene. Promotes eye health.",
    "Good source of fiber. Aids digestion.",
    
    # Pepper benefits (24-27)
    "High in vitamin C. Boosts immunity.",
    "Contains capsaicin. Natural pain reliever.",
    "Rich in antioxidants. Anti-inflammatory properties.",
    "Low calorie. Supports weight management.",
    
    # Potato benefits (28-31)
    "Good source of potassium. Regulates blood pressure.",
    "Contains vitamin B6. Supports brain function.",
    "High in fiber. Promotes gut health.",
    "Rich in antioxidants. Reduces inflammation.",
    
    # Strawberry benefits (32-35)
    "High in vitamin C. Supports collagen production.",
    "Contains ellagic acid. Anti-aging properties.",
    "Rich in antioxidants. Heart health benefits.",
    "Low glycemic index. Good for blood sugar control.",
    
    # Tomato benefits (36-38)
    "Rich in lycopene. Promotes heart health.",
    "High in vitamins A and C. Supports immune system.",
    "Contains antioxidants. Protects skin health."
]

disease_info['fertilizer'] = [
    # Apple fertilizer (0-3)
    "Apply 10-10-10 NPK in spring. Add calcium nitrate in summer.",
    "Use balanced organic fertilizer. Add compost in spring.",
    "Apply phosphorus-rich fertilizer pre-flowering.",
    "Feed with micronutrient mix monthly during growing season.",
    
    # Blueberry fertilizer (4-7)
    "Use acid-forming fertilizers like ammonium sulfate.",
    "Apply organic matter and maintain pH 4.5-5.5.",
    "Feed with balanced fertilizer in spring and summer.",
    "Add iron supplements if leaves yellow.",
    
    # Cherry fertilizer (8-11)
    "Apply 10-10-10 NPK in spring. Add calcium later.",
    "Use organic compost and balanced nutrients.",
    "Feed nitrogen-rich fertilizer in spring.",
    "Add potassium before fruit development.",
    
    # Corn fertilizer (12-15)
    "Apply nitrogen-rich fertilizer at planting.",
    "Side-dress with nitrogen when knee-high.",
    "Use balanced NPK throughout growth.",
    "Add micronutrients based on soil test.",
    
    # Grape fertilizer (16-19)
    "Use 16-16-16 NPK in early spring.",
    "Add magnesium sulfate during growing.",
    "Apply phosphorus before blooming.",
    "Feed potassium for fruit development.",
    
    # Peach fertilizer (20-23)
    "Use balanced fertilizer in spring.",
    "Apply nitrogen after fruit set.",
    "Add calcium for fruit quality.",
    "Feed with micronutrients as needed.",
    
    # Pepper fertilizer (24-27)
    "Start with balanced NPK fertilizer.",
    "Feed calcium to prevent blossom end rot.",
    "Apply magnesium sulfate if leaves yellow.",
    "Use phosphorus for fruit development.",
    
    # Potato fertilizer (28-31)
    "Apply balanced fertilizer at planting.",
    "Side-dress with nitrogen during growth.",
    "Use potassium for tuber development.",
    "Add calcium to prevent scab.",
    
    # Strawberry fertilizer (32-35)
    "Feed balanced NPK before planting.",
    "Apply nitrogen in early spring.",
    "Use phosphorus for flower development.",
    "Add potassium for fruit quality.",
    
    # Tomato fertilizer (36-38)
    "Start with balanced NPK fertilizer.",
    "Feed calcium to prevent blossom end rot.",
    "Apply magnesium sulfate if leaves yellow."
]

def predict_image(image_path):
    # Get filename from path
    filename = os.path.basename(image_path)
    
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    
    # Get prediction details
    title = disease_info['disease_name'][index]
    description = disease_info['description'][index]
    prevent = disease_info['Possible Steps'][index]
    supplement_name = supplement_info['supplement name'][index]
    
    return {
        'disease_name': title,
        'description': description,
        'prevention': prevent,
        'supplement': supplement_name,
        'image_path': f'/static/uploads/{filename}',
        'growing_tips': disease_info['growing_tips'][index],
        'benefits': disease_info['benefits'][index],
        'fertilizer': disease_info['fertilizer'][index]
    }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plant_disease.db'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('profile'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        user = User(
            email=request.form.get('email'),
            password_hash=generate_password_hash(request.form.get('password'))
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('auth/signup.html')

@app.route('/profile')
@login_required
def profile():
    user = current_user
    history = DiseaseHistory.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, history=history)

# Disease History routes
@app.route('/history')
@login_required
def history():
    user = current_user
    history = DiseaseHistory.query.filter_by(user_id=user.id).all()
    return render_template('history.html', history=history)

# Analytics routes
@app.route('/analytics')
@login_required
def analytics():
    user = User.query.filter_by(id=current_user.id).first()
    history = DiseaseHistory.query.filter_by(user_id=user.id).all()
    
    # Process data for charts
    disease_counts = {}
    success_rates = {'Successful': 0, 'Partial': 0, 'Failed': 0}
    monthly_trends = {}

    for entry in history:
        # Disease distribution
        disease_counts[entry.disease_name] = disease_counts.get(entry.disease_name, 0) + 1
        
        # Success rates
        if entry.success_rate >= 80:
            success_rates['Successful'] += 1
        elif entry.success_rate >= 40:
            success_rates['Partial'] += 1
        else:
            success_rates['Failed'] += 1
            
        # Monthly trends
        month_key = entry.diagnosis_date.strftime('%Y-%m')
        monthly_trends[month_key] = monthly_trends.get(month_key, 0) + 1

    analytics_data = {
        'disease_distribution': {
            'labels': list(disease_counts.keys()),
            'data': list(disease_counts.values())
        },
        'success_rates': {
            'labels': list(success_rates.keys()),
            'data': list(success_rates.values())
        },
        'monthly_trends': {
            'labels': list(monthly_trends.keys()),
            'data': list(monthly_trends.values())
        }
    }
    
    return render_template('analytics.html', analytics_data=analytics_data)

# Notification routes
@app.route('/notifications')
@login_required
def notifications():
    user = current_user
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifications)

# Feedback routes
@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        user = current_user
        feedback = Feedback(
            user_id=user.id,
            rating=request.form.get('rating'),
            comment=request.form.get('comment')
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('profile'))
    return render_template('feedback.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detect')
def detect_page():
    return render_template('detect.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/market')
def market():
    return render_template('market.html', 
        supplements=zip(
            supplement_info['supplement image'],
            supplement_info['supplement name'],
            disease_info['disease_name'],
            supplement_info['buy link']
        ))

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get prediction
        prediction_result = predict_image(filepath)
        prediction_result['image_path'] = f'/static/uploads/{filename}'
        
        # Save to history if user is logged in
        if current_user.is_authenticated:
            history = DiseaseHistory(
                user_id=current_user.id,
                disease_name=prediction_result['disease_name'],
                plant_image_url=prediction_result['image_path'],
                treatment_applied=prediction_result['supplement'],
                success_rate=0,  # Initial success rate
                notes="Newly detected disease"
            )
            db.session.add(history)
            db.session.commit()

            # Create notification
            notification = Notification(
                user_id=current_user.id,
                message=f"New disease detected: {prediction_result['disease_name']}"
            )
            db.session.add(notification)
            db.session.commit()
        
        return jsonify(prediction_result)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder
    with app.app_context():
        db.create_all()
    app.run(debug=True)
