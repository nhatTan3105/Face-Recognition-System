
# Face Recognition System

![Face Recognition System](https://cdn-icons-png.flaticon.com/512/1461/1461141.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The **Face Recognition System** is a Python-based project designed to recognize and label faces using the YuNet face detector and SFace recognizer. The system is built with a focus on accuracy, speed, and error reduction, making it ideal for various applications requiring facial recognition capabilities.

This project is part of my thesis, where I aim to evaluate the system's performance across datasets of different sizes and report the findings in terms of accuracy, processing speed, and error rates.

## Features

- **Real-time Face Detection**: Utilizes YuNet for fast and efficient face detection.
- **Accurate Face Recognition**: Employs SFace for recognizing and labeling detected faces.
- **User Interface**: A user-friendly interface built using PyQt5.
- **Performance Evaluation**: Tools to evaluate the system's performance on different datasets.
- **Customizable**: Easily extendable and customizable to fit specific needs.

## Installation

### Prerequisites

Ensure you have Python 3.8.0 installed. The required libraries are listed in `requirements.txt`.

### Steps

1. Clone the repository:
    \`\`\`bash
    git clone https://github.com/nhatTan3105/Face-Recognition-System.git
    cd Face-Recognition-System
    \`\`\`

2. Create a virtual environment:
    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    \`\`\`

3. Install the dependencies:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

4. Run the application:
    \`\`\`bash
    python main.py
    \`\`\`

## Usage

1. **Running the Application**:
    - Launch the application using the command above.
    - The main interface will allow you to start the face detection and recognition process.

2. **Evaluating Performance**:
    - You can use the `sface.py` module to run performance evaluations on different datasets. Customize the datasets and parameters as needed in your evaluation scripts.

## Project Structure

\`\`\`
Face-Recognition-System/
│
├── main.py                   # Entry point for the application
├── sface.py                  # Module for face recognition and evaluation
├── data/
│   ├── data_embeddings.pkl   # Sample data embeddings for testing
│   └── ...                   # Additional datasets
├── ui/                       # User interface components
│   └── main.ui               # PyQt5 UI design file
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── ...
\`\`\`

## Technologies Used

- **Python 3.8.0**
- **OpenCV** for image processing and face detection
- **PyQt5** for the graphical user interface
- **scikit-learn** for data handling and model evaluation
- **YuNet** for face detection
- **SFace** for face recognition

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request if you have any improvements or fixes. You can also open an issue if you encounter any bugs or have feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to contact me:

- **GitHub**: [nhatTan3105](https://github.com/nhatTan3105)
- **Email**: nhattan3105.forwork@gmail.com
