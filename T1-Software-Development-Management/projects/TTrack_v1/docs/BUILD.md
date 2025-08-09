# TTrack Build & Deployment Guide

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone and navigate to project
cd TTrack_v1

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your actual Supabase credentials
```

### 2. Configure Database
Edit your `.env` file with your Supabase credentials:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
DATABASE_TIMEOUT=30
DATABASE_RETRY_ATTEMPTS=3
```

### 3. Run Development
```bash
python main.py
```

## 🏗️ Building for Production

### Prerequisites
- Python 3.8+
- PyInstaller
- All dependencies from `requirements.txt`

### Build Commands

#### Windows
```bash
pyinstaller TTrack.spec
```

#### macOS
```bash
pyinstaller TTrack-macOs.spec
```

### Build Output
- **Executable**: `dist/TTrack` (or `TTrack.exe` on Windows)
- **Includes**: `.env.example` file for user configuration

## 📋 Deployment Checklist

### For End Users
1. ✅ **Executable**: Distribute the built executable
2. ✅ **Environment Template**: Include `.env.example`
3. ✅ **Setup Instructions**: Provide database configuration guide
4. ✅ **Dependencies**: All required libraries bundled

### User Setup Instructions
1. **Download** the TTrack executable
2. **Copy** `.env.example` to `.env` in the same directory
3. **Edit** `.env` with your Supabase credentials:
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   ```
4. **Run** the executable

## 🔧 Build Configuration

### Hidden Imports
The following modules are included as hidden imports for PyInstaller:
- `dotenv` - Environment variable loading
- `supabase` - Database client
- `supabase.client` - Supabase client core
- `postgrest` - PostgreSQL REST API
- `gotrue` - Authentication
- `realtime` - Real-time subscriptions
- `storage3` - File storage

### Data Files
The following files are bundled with the executable:
- Sample academic transcript (`services/data/`)
- Sample curriculum (`services/data/`)
- Application icons (`public/`)
- Environment template (`.env.example`)

## 🐛 Troubleshooting

### Common Build Issues

#### Missing Module Errors
If you get "ModuleNotFoundError" during runtime:
1. Add the missing module to `hiddenimports` in the `.spec` file
2. Rebuild the executable

#### Environment Variable Issues
If database connection fails:
1. Verify `.env` file exists in the same directory as executable
2. Check that `SUPABASE_URL` and `SUPABASE_KEY` are correctly set
3. Ensure no trailing spaces or quotes in environment values

#### Database Connection Errors
If you see "Failed to initialize Supabase client":
1. Verify your Supabase project is active
2. Check that the URL and key are correct
3. Ensure your network connection is stable

## 📦 Distribution

### File Structure
```
TTrack-v3.5.0/
├── TTrack(.exe)           # Main executable
├── .env.example           # Environment template
├── README.md              # User instructions
└── services/data/         # Sample files (bundled)
```

### User Instructions Template
```markdown
# TTrack Setup

1. Copy `.env.example` to `.env`
2. Edit `.env` with your Supabase credentials
3. Run TTrack executable
4. Login with your account
5. Upload transcript and curriculum files
6. Process and download your academic progress data

For support, visit: [your-support-url]
```

## 🔄 Version Management

### Environment Variables by Version
- **v3.4.0**: Basic Supabase integration
- **v3.5.0**: Full `.env` support with validation
- **Future**: Additional database providers, encryption keys

### Build Versioning
Update version numbers in:
- `main.py` (if applicable)
- Build scripts
- Documentation
- Distribution packages

## 🧪 Testing Builds

### Pre-Release Checklist
- [ ] Build completes without errors
- [ ] Executable starts successfully
- [ ] `.env.example` is included in distribution
- [ ] Database connection works with valid credentials
- [ ] Error handling works with invalid/missing credentials
- [ ] All core features functional in built version

### Test Scenarios
1. **Fresh Install**: Test with new `.env` setup
2. **Invalid Credentials**: Verify error handling
3. **Missing .env**: Ensure graceful fallback
4. **Network Issues**: Test offline behavior
