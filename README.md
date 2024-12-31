# **SQLyzer 🕵️‍♂️**

**SQLyzer** is a powerful and user-friendly **SQL Injection Vulnerability Scanner** designed to help developers, security researchers, and bug hunters identify SQL injection vulnerabilities in web applications. With advanced crawling capabilities, multi-threading support, and a modern terminal UI, SQLyzer makes vulnerability scanning efficient and intuitive.

# **If you found any error in this tool, Reach me AS SOON AS POSSIBLE ⚠!**

---

## **Features ✨**

- **Advanced Crawling**: Crawls JavaScript-heavy websites using Selenium for dynamic content.
- **Multi-Threading**: Speeds up scanning by testing multiple URLs simultaneously.
- **Custom Payloads**: Supports custom SQL injection payloads for tailored testing.
- **Proxy Support**: Allows scanning through proxies for anonymity.
- **Verbose Mode**: Provides detailed output for debugging and analysis.
- **Modern UI**: Uses `rich` and `colorama` for a clean and colorful terminal interface.
- **Save Results**: Generates well-formatted reports in a text file.
- **Emoji Support**: Adds visual flair to the terminal and output files.

---

## **Installation 🛠️**

1. Clone the repository:
   ```bash
   git clone https://github.com/darkstarbdx/SQLyzer
   cd SQLyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage 🚀**

Run SQLyzer with the following command:
```bash
python3 sqlyzer.py -u https://example.com
```

### **Options**
- `-u, --url`: Target URL to scan.
- `-p, --payloads`: Path to a file containing custom payloads.
- `-x, --proxy`: Proxy to use for requests (e.g., `http://127.0.0.1:8080`).
- `-v, --verbose`: Enable verbose output.
- `-t, --threads`: Number of threads to use (default: 10).
- `-o, --output`: Save results to a file.
- `-a, --advanced`: Use advanced crawling for JavaScript-heavy sites.
- `-h, --help`: Show the help menu.

### **Example**
```bash
python3 sqlyzer.py -u https://testphp.vulnweb.com -p payloads.txt -x http://127.0.0.1:8080 -v -t 20 -o results.txt -a
```

---

## **Screenshots 📸**

### **Help Menu**
![help](https://github.com/user-attachments/assets/85c819ac-d077-4490-9f29-531c009ee9b7)


### **Scan Results**
![scan](https://github.com/user-attachments/assets/26bde2e2-11e6-4613-992b-65ba985da7ac)


### **Output File**
![output](https://github.com/user-attachments/assets/158735bb-7c55-4053-8512-bb58df7b4db2)

---

## **Support 🆘**

If you encounter any issues or have questions, **reach out to me ASAP**!
✨ Want to get in touch?
🌟 Join our vibrant Telegram community!
👉 Click here to connect: [Telegram Group](https://t.me/+mzZ9IrWgXe9jNWNl)

---

## **License 📜**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgements 🙏**

- **Selenium**: For advanced crawling of JavaScript-heavy websites.
- **Rich**: For creating a modern and colorful terminal UI.
- **Colorama**: For cross-platform colored terminal text.
- **Tqdm**: For progress bars during scanning.

---

## **Happy Hacking! 🚀**

SQLyzer is here to make your SQL injection vulnerability scanning easier and more efficient. If you find this tool useful, don’t forget to ⭐ the repository and share it with others!
