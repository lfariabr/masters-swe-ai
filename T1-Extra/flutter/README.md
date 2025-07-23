# Flutter Lumen.gg app

## Setup
- Open Terminal and run:
brew install --cask flutter
Wait for a few minutes, it should pop "🍺  flutter was successfully installed!"

- Check if installed correctly and the version:
flutter --version

- Install Flutter extension for VSCode:
macOS: cmd + shift + p: Flutter
Windows: ctrl + shift + p: Flutter

- Run flutter doctor to check the setup:
flutter doctor

- Create config for flutter:
sudo mkdir -p ~/.config/flutter
sudo chown -R $(whoami) ~/.config

- Now run flutter doctor again:
flutter doctor

### Route 1: To run on chrome

- Create the project
flutter create lumin_demo
cd lumin_demo
code .

- Run on chrome:
flutter run -d chrome

### Route 2: To run on iOS simulator

- Install Xcode from Appstore

- Install CocoaPods:
sudo gem install cocoapods

# Tech Stack
- Framework: Flutter
- State Management: Provider
- API Layer: Dio package
- Architecture: Loosely based on MVVM
- Navigation / Routing: Custom (Recommend using the inbuilt material router when learning and moving onto Go-router if you want to learn about deep linking and/or advanced routing)
- Platforms: iOS, Android, Web

# Goals
Lumin is the ultimate gaming social platform—a space where gamers can upload, watch, and engage with their best gaming moments. Only gaming clips. No other content. No distractions