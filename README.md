# 🔧 Android Mod Menu Auto Injector

A professional automation utility designed to simplify the integration of **mod menus into Unity IL2CPP Android games**.  
This tool reduces manual work by automatically modifying required files inside a **decompiled APK project**.

---

## 📌 Overview

**Android Mod Menu Auto Injector** is built for developers and modders who work with **Unity IL2CPP games**.  
It automates common tasks required when injecting a mod menu framework into Android applications.

Instead of manually editing multiple files, this tool performs the necessary modifications **quickly, consistently, and reliably**.

---

## ✨ Features

- ⚙️ **Automatic AndroidManifest Modification**  
  Injects required services, permissions, and configuration entries.

- 🧩 **Smali Code Injection**  
  Automatically inserts mod menu initialization into the main activity.

- 🖥 **Mod Menu Service Setup**  
  Configures the service required to launch and maintain the mod menu.

- 🔐 **Permission Injection**  
  Adds overlay and other necessary permissions for mod menu functionality.

- 📂 **Automatic Library Copying**  
  Places required `.so` libraries and mod menu files into the correct directories.

---

## 🧰 Requirements

Before using the injector, ensure you have:

- A **decompiled APK project**
- Basic knowledge of **Android APK modification**
- Standard reverse engineering tools installed

### Required Tools

```
APKTool
Java / JDK
Python 3.x (if running the Python version of the injector)
```

---

## 🚀 Usage

### 1️⃣ Decompile the Target APK

```bash
apktool d game.apk
```

### 2️⃣ Launch the Injector Tool

Run the injector executable or script.

### 3️⃣ Select the Decompiled APK Folder

Browse and select the folder created after APK decompilation.

### 4️⃣ Click **Inject**

The tool will automatically perform all required modifications.

---

## 📁 Files Modified

During injection, the following components are modified automatically:

```
AndroidManifest.xml
Main Activity smali file
Mod menu service configuration
Required mod menu libraries
Mod menu assets and resources
```

---

## ⚙️ Automated Injection Tasks

The injector performs the following operations internally:

```
✔ Modify AndroidManifest.xml
✔ Inject mod menu service
✔ Add required permissions
✔ Locate and modify main activity smali
✔ Inject mod menu initialization
✔ Copy required .so libraries
✔ Copy mod menu resource files
```

---

## 📂 Typical Workflow

```
Original APK
     │
     ▼
Decompile with APKTool
     │
     ▼
Run Android Mod Menu Auto Injector
     │
     ▼
Automatic Manifest + Smali Injection
     │
     ▼
Recompile APK
     │
     ▼
Sign and Install
```

---

## 🔒 Disclaimer

This software is provided for **educational and research purposes only**.

Use this tool **only on applications you own or have explicit permission to modify**.  
The developer assumes **no responsibility for misuse or damage caused by this tool**.

---

## 👤 Author

**lolakulu**

---

## 📬 Contact

**Email**

```
jhaprabhat884@gmail.com
```

---

## 🎥 YouTube

```
https://www.youtube.com/@secrettech9186
```

---

## 💻 GitHub

```
https://github.com/CertifiedSomebody
```

---

## 🧩 Platinmods Profile

```
https://platinmods.com/members/lolakulu.4441950/
```

---

⭐ If you find this project useful, consider supporting the work by following on **YouTube, GitHub, or Platinmods**.
