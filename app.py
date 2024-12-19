# Important Imports
import os
import re  
import fitz  # PyMuPDF

# Flask Application Import
from flask import Flask, request, render_template, redirect, url_for
# Import for Getting Closer Matches from the resume text
from difflib import get_close_matches


# This will store the uploaded files in a temporary folder name TEMP_FOLDER and Ranks the resume there
app = Flask(__name__)
# Upload Folder
app.config['UPLOAD_FOLDER'] = 'uploads'
# Temp Resume Store
app.config['TEMP_FOLDER'] = os.path.join(os.path.dirname(__file__), 'temp_uploads')

job_roles = {

    # Preferred Skills for Full Stack Developer
    "Full Stack Developer": [
        "html", "css", "javascript", "mongodb", "express", "angular", "react", "node", "PHP", "MySql", "python",
        "databases", "bootstrap", "ruby", ".NET", "Django", "Git", "Github", "GitLabs", "Apache", "RestfulAPI",
        "Docker", "cloud", "kubernetes", "OAuth", "jest", "Typescript", "Webpack", "Babel", "GraphQL", "Redis",
        "CouchDB", "Nginx", "Heroku", "AWS", "GCP", "Azure", "SASS", "LESS"
    ],
# Preferred Skills for Front End Developer
    "Frontend Developer": [
        "html", "css", "javascript", "react", "angular", "vue.js", "jQuery", "bootstrap", "tailwind", "tailwind CSS",
        "restful api", "git", "github", "npm", "yarn", "SASS", "LESS", "Typescript", "Webpack", "Babel", "GraphQL",
        "Redux", "Next.js", "Gatsby", "Ember.js", "Backbone.js", "Handlebars.js", "PWA", "Webpack"
    ],

    # Preferred Skills for BackEnd Developer

    "Backend Developer": [
        "node", "express", "mongodb", "mysql", "postgresql", "python", "django", "flask", "ruby on rails", "java",
        "spring", "PHP", "laravel", "C#", ".NET", "kotlin", "scala", "go", "Rust", "GraphQL", "RestfulAPI",
        "Redis", "Docker", "Kubernetes", "Nginx", "AWS", "GCP", "Azure", "Elasticsearch", "RabbitMQ", "Kafka",
        "Jenkins", "CI/CD", "Git", "Github", "Gitlab", "Terraform"
    ],
# Preferred Skills for AI & ML Engineer
    "AI & ML Engineer": [
        "python", "tensorflow", "pytorch", "scikit-learn", "machine learning", "deep learning", "neural networks",
        "numpy", "pandas", "keras", "matplotlib", "seaborn", "opencv", "nlp", "R", "xgboost", "lightgbm", "catboost",
        "jupyter", "colab", "docker", "flask", "fastapi", "sql", "mongodb", "AWS", "GCP", "Azure", "Sagemaker",
        "Kubeflow", "Mlflow", "Huggingface", "transformers"
    ],

# Preferred Skills for Python Developer
    
    "Python Developer": [
        "python", "django", "flask", "fastapi", "sqlalchemy", "numpy", "pandas", "scipy", "matplotlib", "seaborn",
        "plotly", "dash", "openpyxl", "selenium", "beautifulsoup", "scrapy", "tensorflow", "pytorch", "keras",
        "scikit-learn", "opencv", "requests", "pytest", "unittest", "pydantic", "SQL", "PostgreSQL", "MySQL",
        "MongoDB", "Redis", "docker", "kubernetes", "aws", "azure", "gcp", "Git", "Github", "Gitlab", "CI/CD",
        "jupyter", "colab", "RestfulAPI", "graphQL", "asyncio", "Celery", "RabbitMQ", "Kafka"
    ],
# Preferred Skills for Android Developer
    "Android App Developer": [
        "java", "kotlin", "android sdk", "android studio", "gradle", "xml", "jetpack", "android jetpack", "mvvm",
        "mvp", "retrofit", "dagger", "hilt", "rxjava", "coroutines", "room", "sqlite", "firebase", "google play services",
        "material design", "restful api", "json", "git", "github", "CI/CD", "espresso", "junit", "mockito"
    ],
# Preferred Skills for IOS Developer
    "IOS App Developer": [
        "swift", "objective-c", "xcode", "cocoa touch", "swiftui", "uikit", "core data", "grand central dispatch",
        "combine", "alamofire", "realm", "sqlite", "firebase", "mapkit", "core location", "cloudkit", "restful api",
        "json", "git", "github", "CI/CD", "testflight", "fastlane", "junit", "xctest"
    ],
# Preferred Skills Data Scientist
    "Data Scientist": [
        "python", "r", "machine learning", "deep learning", "neural networks", "numpy", "pandas", "scikit-learn",
        "tensorflow", "pytorch", "keras", "matplotlib", "seaborn", "plotly", "statsmodels", "nltk", "spacy", "opencv",
        "sql", "postgresql", "mysql", "mongodb", "big data", "hadoop", "spark", "databricks", "aws", "azure", "gcp",
        "docker", "jupyter", "colab", "sagemaker", "kubeflow", "mlflow"
    ],
# Preferred Skills for Data Analyst
    "Data Analyst": [
        "python", "r", "sql", "tableau", "power bi", "excel", "numpy", "pandas", "matplotlib", "seaborn", "plotly",
        "statistics", "machine learning", "regression", "clustering", "sql", "postgresql", "mysql", "mongodb",
        "big data", "hadoop", "spark", "databricks", "aws", "azure", "gcp", "ETL", "data warehousing", "data mining"
    ],
# Preferred Skills for Cyber Security Engineer
    "Cyber Security Engineer": [
        "network security", "application security", "cloud security", "firewalls", "ids", "ips", "SIEM", "Vulnerability assessment",
        "Penetration testing", "ethical hacking", "cryptography", "threat modeling", "risk assessment", "compliance",
        "ISO 27001", "NIST", "OWASP", "CEH", "CISSP", "SSL/TLS", "PKI", "IAM", "Azure security", "AWS security", "GCP security",
        "Python", "Bash", "Powershell", "Metasploit", "Nmap", "Wireshark", "Kali Linux"
    ],
# Preferred Skills for Network Engineer
    "Network Engineer": [
        "TCP/IP", "DNS", "DHCP", "VLANs", "Routing", "Switching", "BGP", "OSPF", "EIGRP", "MPLS", "VPN", "Firewall",
        "IDS", "IPS", "Load balancers", "QoS", "Network monitoring", "Wireshark", "Cisco", "Juniper", "Aruba", "Fortinet",
        "Python", "Bash", "Powershell", "Ansible", "Terraform", "Cloud networking", "AWS", "Azure", "GCP"
    ],
# Preferred Skills for Mobile Developer
    "Mobile Developer": [
        "java", "kotlin", "swift", "objective-c", "react native", "flutter", "dart", "android sdk", "ios sdk",
        "xcode", "android studio", "material design", "ui/ux design", "restful api", "json", "git", "github",
        "CI/CD", "firebase", "sqlite", "realm", "mvvm", "mvp", "rxjava", "coroutines", "flutter widgets"
    ],
# Preferred Skills for Cloud Engineer
    "Cloud Engineer": [
        "AWS", "Azure", "GCP", "cloud architecture", "cloud security", "virtualization", "Docker", "Kubernetes",
        "Terraform", "Ansible", "CI/CD", "Jenkins", "Git", "Github", "Gitlab", "Linux", "Windows Server",
        "Python", "Bash", "Powershell", "Networking", "Load balancers", "DNS", "IAM", "CloudFormation", "ARM Templates"
    ],
# Preferred Skills for Cloud Architect
    "Cloud Architect": [
        "AWS", "Azure", "GCP", "cloud architecture", "cloud security", "cloud strategy", "virtualization", "Docker",
        "Kubernetes", "Terraform", "Ansible", "CI/CD", "Jenkins", "Git", "Github", "Gitlab", "Linux", "Windows Server",
        "Python", "Bash", "Powershell", "Networking", "Load balancers", "DNS", "IAM", "CloudFormation", "ARM Templates",
        "microservices", "serverless", "cost management", "performance optimization"
    ],
# Preferred Skills for DevOps Engineer
    "DevOps Engineer": [
        "CI/CD", "Jenkins", "Git", "Github", "Gitlab", "Docker", "Kubernetes", "Ansible", "Terraform", "AWS", "Azure",
        "GCP", "Linux", "Windows Server", "Python", "Bash", "Powershell", "Monitoring", "Prometheus", "Grafana",
        "Nagios", "Splunk", "Log management", "Automation", "Infrastructure as Code", "Agile", "Scrum"
    ],
 # Preferred Skills for Product Manager
    "Product Manager": [
        "product lifecycle", "roadmapping", "agile", "scrum", "kanban", "user stories", "backlog management",
        "stakeholder management", "market research", "competitive analysis", "product strategy", "MVP", "A/B testing",
        "user experience", "data analysis", "sql", "excel", "JIRA", "Confluence", "Trello", "Asana", "communication",
        "leadership", "problem solving", "strategic thinking"
    ],
# Preferred Skills for UI / UX Designer
    "UI/UX Designer": [
        "ui design", "ux design", "wireframing", "prototyping", "user research", "user testing", "interaction design",
        "visual design", "adobe xd", "sketch", "figma", "invision", "photoshop", "illustrator", "html", "css",
        "javascript", "responsive design", "accessibility", "design thinking", "information architecture", "user personas",
        "journey mapping", "heuristic evaluation"
    ],
# Preferred Skills for Software Engineer
     "Software Engineer": [
        "programming languages", "algorithms", "data structures", "software development", "debugging", 
        "problem-solving", "object-oriented design", "system design", "coding", "testing", "agile", 
        "scrum", "git", "github", "docker", "linux", "communication skills"
    ],
# Preferred Skills for System Architect
    "Systems Architect": [
        "system architecture", "cloud computing", "networking", "virtualization", "security", 
        "databases", "integration", "performance tuning", "scalability", "reliability", "disaster recovery", 
        "enterprise architecture", "system modeling", "system design", "automation", "problem-solving"
    ],
# Preferred Skills for Database Adminstrator
    "Database Administrator": [
        "database management", "SQL", "NoSQL", "database design", "database security", "database tuning", 
        "data modeling", "backup and recovery", "performance monitoring", "data warehousing", 
        "ETL (Extract, Transform, Load)", "SQL Server", "Oracle", "MySQL", "PostgreSQL", "MongoDB"
    ],
# Preferred Skills for Software Tester
    "Software Tester": [
        "test planning", "test case design", "test automation", "manual testing", "automated testing", 
        "regression testing", "performance testing", "load testing", "integration testing", "user acceptance testing", 
        "defect tracking", "agile testing", "ISTQB", "Selenium", "JUnit", "TestNG"
    ],
# Preferred Skills for Systems Analyst
    "Systems Analyst": [
        "system analysis", "requirements gathering", "system design", "system modeling", "data analysis", 
        "business process modeling", "workflow analysis", "problem-solving", "communication skills", 
        "documentation", "agile", "UML", "SQL", "SDLC", "user stories", "user acceptance testing"
    ],
# Preferred Skills for Game Developer
    "Game Developer": [
        "game development", "game design", "Unity", "Unreal Engine", "C#", "C++", "3D modeling", 
        "animation", "physics in games", "AI in games", "multiplayer games", "game optimization", 
        "mobile game development", "console game development", "game testing", "virtual reality (VR)"
    ],
# Preferred Skills for Embedded Systems Engineer
    "Embedded Systems Engineer": [
        "embedded systems", "microcontrollers", "RTOS", "embedded C", "firmware development", "hardware design", 
        "sensors", "actuators", "communication protocols", "I2C", "SPI", "UART", "CAN bus", "debugging", 
        "real-time systems", "system integration"
    ],
# Preferred Skills for Data Engineer
    "Data Engineer": [
        "big data", "data pipelines", "ETL (Extract, Transform, Load)", "data modeling", "data warehousing", 
        "data lakes", "SQL", "NoSQL", "Hadoop", "Spark", "Kafka", "stream processing", "Python", 
        "Scala", "Java", "cloud computing", "AWS", "Azure", "GCP"
    ],
# Preferred Skills for Cloud Solutions Architect
    "Cloud Solutions Architect": [
        "cloud computing", "AWS", "Azure", "GCP", "cloud architecture", "serverless computing", "microservices", 
        "containerization", "Kubernetes", "Docker", "security", "networking", "IAM", "cloud migration", 
        "cost optimization", "compliance"
    ],
# Preferred Skills for Security Analyst
    "Information Security Analyst": [
        "information security", "network security", "cybersecurity", "security policies", "vulnerability assessment", 
        "penetration testing", "incident response", "firewalls", "encryption", "SIEM", "risk management", 
        "compliance", "security audits", "ethical hacking", "CISSP", "CISM", "CEH"
    ],
# Preferred Skills for BlockChain Developer
    "Blockchain Developer": [
        "blockchain", "smart contracts", "cryptocurrency", "Ethereum", "Solidity", "dApps", "blockchain security", 
        "decentralized systems", "consensus algorithms", "Hyperledger", "R3 Corda", "web3.js", "truffle", 
        "ganache", "blockchain scalability", "tokenomics"
    ],
# Preferred Skills for Site Reliability Engineer
    "Site Reliability Engineer (SRE)": ["site reliability engineering", "system administration", "cloud computing", "automation", "monitoring", "incident response", "capacity planning", "CI/CD", "Kubernetes", "Docker", "AWS", "GCP", "Azure", "Linux", "Python", "Bash", "Powershell", "Networking", "Load balancers", "DNS", "IAM", "CloudFormation", "ARM Templates"],
# Preferred Skills for Systems Architect
    "Systems Architect": [
        "system architecture", "enterprise architecture", "cloud architecture", "network architecture",
        "security architecture", "solution architecture", "TOGAF", "AWS", "Azure", "GCP", "Docker", "Kubernetes",
        "Terraform", "Python", "Java", "C#", "SQL", "NoSQL", "RESTful APIs", "Microservices"
    ],

    # Preferred Skills for Hardware Engineer
    "Hardware Engineer": [
        "computer hardware", "electronics", "digital circuits", "analog circuits", "microprocessors",
        "microcontrollers", "embedded systems", "FPGA", "ASIC", "PCB design", "signal processing", "C", "C++",
        "VHDL", "Verilog", "MATLAB"
    ],
    # Preferred Skills for Computer Vision Engineer
    "Computer Vision Engineer": [
        "computer vision", "image processing", "video processing", "deep learning", "neural networks", "OpenCV",
        "TensorFlow", "PyTorch", "CUDA", "C++", "Python", "MATLAB"
    ],

    # Preferred Skills for IT Operations Manager
    "IT Operations Manager": [
        "IT operations", "network administration", "system administration", "ITIL", "incident management",
        "problem management", "change management", "service desk management", "vendor management", "budget management",
        "team leadership", "communication skills"
    ],

    # Preferred Skills for CRM Developer
    "CRM Developer": [
        "CRM", "customer relationship management", "Salesforce", "Microsoft Dynamics", "SAP CRM", "Oracle CRM",
        "CRM customization", "CRM integration", "CRM analytics", "JavaScript", "Apex", "SQL", "web services"
    ],
    # Preferred Skills for AR Developer
    "Augmented Reality (AR) Developer": [
        "augmented reality", "ARKit", "ARCore", "Unity", "3D modeling", "C#", "C++", "JavaScript", "UI/UX design",
        "computer vision", "mobile development"
    ],
    # Preferred Skills for VR Developer
    "Virtual Reality (VR) Developer": [
        "virtual reality", "Unity", "Unreal Engine", "C#", "C++", "3D modeling", "UI/UX design", "game development",
        "immersive experiences", "interactive simulations"
    ],
    # Preferred Skills for Robotics Engineer
    "Robotics Engineer": [
        "robotics", "robotic systems", "robotic programming", "ROS", "MATLAB", "Python", "C++", "control systems",
        "sensor fusion", "mechatronics", "AI", "computer vision"
    ],

    # Preferred Skills for NLP Engineer
    "Natural Language Processing (NLP) Engineer": [
        "natural language processing", "NLP", "machine learning", "deep learning", "neural networks", "Python",
        "NLTK", "spaCy", "Stanford NLP", "Gensim", "word embeddings", "sentiment analysis", "text classification",
        "information retrieval"
    ],

    # Preferred Skills for Big Data Engineer
    "Big Data Engineer": [
        "big data", "Hadoop", "Spark", "Kafka", "Hive", "Pig", "HBase", "MapReduce", "Scala", "Python", "Java", "SQL",
        "NoSQL", "data pipelines", "data warehousing", "ETL"
    ],

    # Preferred Skills for Computer Graphics Engineer
    "Computer Graphics Engineer": [
        "computer graphics", "OpenGL", "DirectX", "GPU programming", "shaders", "3D rendering", "C++", "Python",
        "Unity", "Unreal Engine", "MATLAB"
    ],

    # Preferred Skills for System Integration Engineer
    "Systems Integration Engineer": [
        "systems integration", "system architecture", "networking", "APIs", "integration testing", "CI/CD",
        "cloud computing", "docker", "kubernetes", "Python", "Java", "C#", "SQL", "NoSQL"
    ],

    # Preferred Skills for Digital Marketing Specialist
    "Digital Marketing Specialist": [
        "digital marketing", "SEO", "SEM", "PPC", "email marketing", "social media marketing", "content marketing",
        "Google Analytics", "marketing automation", "conversion rate optimization", "web analytics", "A/B testing",
        "copywriting", "graphic design"
    ],
    # Preferred Skills for SEO Specialist 
    "SEO Specialist": [
        "SEO", "search engine optimization", "keyword research", "on-page SEO", "off-page SEO", "link building",
        "SEO tools", "Google Analytics", "Google Search Console", "SEO audits", "content optimization", "technical SEO",
        "local SEO", "e-commerce SEO"
    ]
}

# It Will Extract the Text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # pdf path
        pdf_document = fitz.open(pdf_path)
        # pdf document
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
    except Exception as e:
        # Text Extraction from PDF
        print(f"Error extracting text from PDF: {e}")
    return text
# Extract CGPA SCORE
def extract_cgpa(text):
    # CGPA Pattern
    cgpa_pattern = re.compile(r"(?i)(cgpa|gpa)\s*[:\-]?\s*(\d+\.\d+)")
    match = cgpa_pattern.search(text)
    if match:
        return float(match.group(2))
    return 0

# Ranking
def rank_resumes(resume_folder, job_description):
    resume_files = os.listdir(resume_folder)
    resumes = []

    # Extract data from each resume
    for resume_file in resume_files:
        if resume_file.endswith(".pdf"):
            resume_path = os.path.join(resume_folder, resume_file)
            text = extract_text_from_pdf(resume_path)

            cgpa = extract_cgpa(text)
            if job_description in job_roles:
                skills_count = sum(text.lower().count(keyword) for keyword in job_roles[job_description])
            else:
                closest_match = find_closest_match(job_description)
                if closest_match:
                    skills_count = sum(text.lower().count(keyword) for keyword in job_roles[closest_match])
                else:
                    skills_count = 0
            exp_count = text.lower().count("experience") + text.lower().count("internship")
# Resume Ranking Details Fetch
            resumes.append({
                "file": resume_file,
                "cgpa": cgpa,
                "skills_count": skills_count,
                "exp_count": exp_count,
            })

    # Rank each resume based on the three criteria
    for criteria in ['skills_count', 'cgpa', 'exp_count']:
        max_value = max(resume[criteria] for resume in resumes)
        for resume in resumes:
            if max_value > 0:
                resume[criteria + '_score'] = 5 * (resume[criteria] / max_value)  # Scale the score to be between 1 and 5
            else:
                resume[criteria + '_score'] = 0

    # Calculate total score for each resume
    for resume in resumes:
        resume['total_score'] = round(resume['cgpa_score'] +
                                      resume['skills_count_score'] +
                                      resume['exp_count_score'], 2)  # Round to 2 decimal places

    # Sort resumes by total score
    ranked_resumes = sorted(resumes, key=lambda x: (x['total_score'], x['skills_count'], x['cgpa'], x['exp_count']), reverse=True)

    return ranked_resumes


    # Rank each resume based on the three criteria
    for criteria in ['skills_count', 'cgpa', 'exp_count']:
        max_value = max(resume[criteria] for resume in resumes)
        for resume in resumes:
            if max_value > 0:
                resume[criteria + '_score'] = 5 * (resume[criteria] / max_value)  # Scale the score to be between 1 and 5
            else:
                resume[criteria + '_score'] = 0

    # Calculate total score for each resume
    for resume in resumes:
        resume['total_score'] = (resume['cgpa_score'] +
                                 resume['skills_count_score'] +
                                 resume['exp_count_score'])

    # Sort resumes by total score
    ranked_resumes = sorted(resumes, key=lambda x: (x['total_score'], x['skills_count'], x['cgpa'], x['exp_count']), reverse=True)

    return ranked_resumes


    # Rank each resume based on the three criteria

    # Ranking is Based on some criteria like Skills Count (The Total no of Relative skills candidate have as per the given job role), CGPA SCORE, Experience Count
    for criteria in ['skills_count', 'cgpa', 'exp_count']:
        max_value = max(resume[criteria] for resume in resumes)
        for resume in resumes:
            if max_value > 0:
                resume[criteria + '_score'] = 1 if resume[criteria] == max_value else 0
            else:
                resume[criteria + '_score'] = 0

    # Calculate total score for each resume
    for resume in resumes:
        resume['total_score'] = (resume['cgpa_score'] +
                                 resume['skills_count_score'] +
                                 resume['exp_count_score'])

    # Sort resumes by total score
    ranked_resumes = sorted(resumes,
                             key=lambda x: (x['total_score'], x['skills_count'], x['cgpa'], x['exp_count']),
                             reverse=True)

    return ranked_resumes

# This will find the closest match of user input job role name
def find_closest_match(user_input):
    closest_matches = get_close_matches(user_input, job_roles.keys(), n=1, cutoff=0.6)
    return closest_matches[0] if closest_matches else None

# Flask Application route default page
@app.route('/')
def index():
    return render_template('index.html')
# Upload PDF file post method
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resumes' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('resumes')
    job_description = request.form.get('job_description', '')
# if there is no upload folder it will create one 
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    for file in files:
        if file.filename.endswith('.pdf'):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return redirect(url_for('ranked_resumes', job_description=job_description))

# It will reset the uploaded folder and also delte the data that was stored in Temp_Folders
@app.route('/reset_temp_uploads', methods=['GET', 'POST'])
def reset_temp_uploads():
    if request.method == 'POST':
        # Clear the contents of the temp_uploads folder
        for filename in os.listdir(app.config['TEMP_FOLDER']):
            file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
# Redirection to File Path
        return redirect(url_for('index'))  
    else:
        return redirect(url_for('index'))  
# it will redirect to the Ranked Resumes page where the ranking will be displayed in the Tabular format with complete analysis of Skills Score, Experience Score and CGPA Score
@app.route('/ranked_resumes', methods=['GET', 'POST'])
def ranked_resumes():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '')
        ranked_resumes = rank_resumes(app.config['UPLOAD_FOLDER'], job_description)
        return render_template('ranked_resumes.html', resumes=ranked_resumes, job_description=job_description, enumerate=enumerate)
    else:
        return render_template('ranked_resumes.html', resumes=[], job_description='', enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)




    


