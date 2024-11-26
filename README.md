### Dataset README for **Phishing URL Content Dataset**

---

#### **Executive Summary**

**Motivation:**  
Phishing attacks are one of the most significant cyber threats in today’s digital era, tricking users into divulging sensitive information like passwords, credit card numbers, and personal details. This dataset aims to support research and development of machine learning models that can classify URLs as phishing or benign. 

**Applications:**  
- Building robust phishing detection systems.  
- Enhancing security measures in email filtering and web browsing.  
- Training cybersecurity practitioners in identifying malicious URLs.  

The dataset contains diverse features extracted from URL structures, HTML content, and website metadata, enabling deep insights into phishing behavior patterns.

---

#### **Description of Data**

This dataset comprises two types of URLs:  
1. **Phishing URLs:** Malicious URLs designed to deceive users.
2. **Benign URLs:** Legitimate URLs posing no harm to users.

**Key Features:**  
- **URL-based features:** Domain, protocol type (HTTP/HTTPS), and IP-based links.  
- **Content-based features:** Link density, iframe presence, external/internal links, and metadata.  
- **Certificate-based features:** SSL/TLS details like validity period and organization.  
- **WHOIS data:** Registration details like creation and expiration dates.

**Statistics:**  
- **Total Samples:** 800 (400 phishing, 400 benign).  
- **Features:** 22 including URL, domain, link density, and SSL attributes.

---

#### **Power Analysis**

To ensure statistical reliability, a power analysis was conducted to determine the minimum sample size required for binary classification with 22 features. Using a medium effect size (0.15), alpha = 0.05, and power = 0.80, the analysis indicated a minimum sample size of ~325 per class. Our dataset exceeds this requirement with 400 examples per class, ensuring robust model training.

---

#### **Exploratory Data Analysis (EDA)**

**Insights from EDA:**  
- **Distribution Plots:** Histograms and density plots for numerical features like link density, URL length, and iframe counts.
- **Bar Plots:** Class distribution and protocol usage trends.
- **Correlation Heatmap:** Highlights relationships between numerical features to identify multicollinearity or strong patterns.
- **Box Plots:** For SSL certificate validity and URL lengths, comparing phishing versus benign URLs.

EDA visualizations are provided in the repository.

---

#### **Link to Publicly Available Data and Code**

- **Dataset:** [Phishing URL Dataset](https://www.kaggle.com/datasets/aaditeypillai/phishing-website-content-dataset/data)  
- **Code Repository:** [GitHub - Phishing Detection](https://github.com/aaditey932/Phishing-URL-Content-Dataset)  

The repository contains the Python code used to extract features, conduct EDA, and build the dataset.

---

#### **Ethics Statement**

Phishing detection datasets must balance the need for security research with the risk of misuse. This dataset:  
1. **Protects User Privacy:** No personally identifiable information is included.  
2. **Promotes Ethical Use:** Intended solely for academic and research purposes.  
3. **Avoids Reinforcement of Bias:** Balanced class distribution ensures fairness in training models.

**Risks:**  
- Misuse of the dataset for creating more deceptive phishing attacks.  
- Over-reliance on outdated features as phishing tactics evolve.

Researchers are encouraged to pair this dataset with continuous updates and contextual studies of real-world phishing.

---

#### **Open Source License**

This dataset is shared under the **MIT License**, allowing free use, modification, and distribution for academic and non-commercial purposes. License details can be found [here](https://opensource.org/licenses/MIT).

--- 

This README ensures clear documentation, statistical rigor, and ethical compliance while enabling impactful research on phishing detection.
