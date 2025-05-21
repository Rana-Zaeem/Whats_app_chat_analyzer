# Deployment Troubleshooting Guide

This document contains instructions for fixing common deployment issues with the WhatsApp Chat Analyzer project.

## Quick Fix Instructions

If you're experiencing deployment errors, follow these steps:

1. **Use the correct Python version**:
   - We've set Python 3.8.18 in `runtime.txt` - this is the most compatible version
   - Do not use Python 3.13 or other very new versions - many dependencies aren't ready yet

2. **Deploy with the fixed requirements**:
   - Use `requirements-fixed.txt` instead of the original requirements file
   - These packages have been tested to work together without conflicts

3. **Fix system dependencies**:
   - Ensure `python3-distutils` is installed in your environment
   - The updated `packages.txt` and `setup.sh` should handle this automatically

## Common Deployment Errors

### "No module named 'distutils'" Error

This happens because modern Python versions often don't include distutils by default. Our setup.sh now:
- Installs python3-distutils automatically
- Uses compatible pip and setuptools versions

### Slow Deployment / Build Failures

This typically happens due to:
- Incompatible package versions requiring rebuilds from source code
- Missing binary wheels for your Python version
- Dependency conflicts

The fixed requirements use only packages with existing wheels for Python 3.8.

## Testing Your Deployment

1. First, test with the minimal app:
   ```
   streamlit run test_app.py
   ```

2. If that works, try the full app:
   ```
   streamlit run app.py
   ```

## Platform-Specific Instructions

### Streamlit Cloud (Recommended)
- Simply push all these files to your repository
- Streamlit Cloud will use the runtime.txt and requirements-fixed.txt automatically

### Heroku
- Ensure you have both `Procfile` and `runtime.txt` in your repository
- If using the Heroku CLI, deploy with:
  ```
  heroku create your-app-name
  git push heroku main
  ```

### Local Development
- Create a virtual environment with Python 3.8:
  ```
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements-fixed.txt
  streamlit run app.py
  ```

## Still Having Issues?

If deployment still fails:
1. Try the minimal test_app.py to isolate the issue
2. Check deployment logs for specific package failures
3. Consider a simpler deployment platform like Streamlit Community Cloud
