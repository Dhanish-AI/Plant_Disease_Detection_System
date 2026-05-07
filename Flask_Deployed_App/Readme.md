# Plant Disease Detection Web Application 🌿

A Flask-based web application that uses deep learning (CNN) to detect plant diseases and provide comprehensive care recommendations.

## Key Features 🌟

- **Disease Detection**: Real-time detection of 39 different plant diseases
- **Care Instructions**: Customized growing tips and treatment plans
- **Analytics Dashboard**: Track disease history and treatment success rates
- **User Management**: Secure authentication and personalized history
- **Notifications**: Real-time alerts for disease detection and treatment reminders
- **Market Integration**: Recommended supplements and treatments

## Supported Plants & Diseases 🌱

1. **Apple**
   - Apple Scab
   - Black Rot
   - Cedar Apple Rust
   - Healthy

2. **Blueberry**
   - Healthy

3. **Cherry**
   - Powdery Mildew
   - Healthy

4. **Grape**
   - Black Rot
   - Esca (Black Measles)
   - Leaf Blight
   - Healthy

5. **Peach**
   - Bacterial Spot
   - Healthy

6. **Pepper**
   - Bacterial Spot
   - Healthy

7. **Potato**
   - Early Blight
   - Late Blight
   - Healthy

8. **Strawberry**
   - Leaf Scorch
   - Healthy

9. **Tomato**
   - Bacterial Spot
   - Early Blight
   - Late Blight
   - Leaf Mold
   - Septoria Leaf Spot
   - Spider Mites
   - Target Spot
   - Yellow Leaf Curl Virus
   - Mosaic Virus
   - Healthy

## Technical Stack 💻

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Model**: PyTorch CNN
- **Authentication**: Flask-Login
- **Charts**: Chart.js

## Installation 🚀

1. Clone the repository:
bash
git clone <repository-url>
cd Flask Deployed App

2. Create and activate virtual environment:
bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

3. Install dependencies:
bash
pip install -r requirements.txt

4. Initialize database:
bash
python
>>> from app import app, db
>>> with app.app_context():
>>> db.create_all()

5. Run the application:
bash
python app.py

## Project Structure 📁

Flask Deployed App/
├── static/
│ ├── uploads/ # Image uploads
│ ├── js/
│ │ └── chart.min.js # Charts visualization
│ └── css/ # Styling files
├── templates/
│ ├── auth/
│ │ ├── login.html
│ │ └── signup.html
│ ├── base.html
│ ├── detect.html
│ ├── analytics.html
│ └── history.html
├── app.py # Main application
├── auth.py # Authentication logic
├── models.py # Database models
├── CNN.py # Neural network model
└── requirements.txt

## Usage Guide 📖

1. **Registration/Login**
   - Create account or login to existing account
   - Access personalized dashboard

2. **Disease Detection**
   - Upload plant leaf image
   - Receive instant disease detection
   - View detailed care recommendations

3. **Treatment Tracking**
   - Monitor disease history
   - Track treatment success rates
   - Receive care notifications

4. **Analytics**
   - View disease distribution charts
   - Track treatment success rates
   - Monitor monthly trends

## API Endpoints 🔌

- `/predict` - POST: Upload image for disease detection
- `/analytics` - GET: View disease statistics
- `/history` - GET: View treatment history
- `/notifications` - GET: View system notifications

## Contributing 🤝

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.