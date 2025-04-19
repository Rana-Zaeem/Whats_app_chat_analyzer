# Deployment Guide for WhatsApp Chat Analyzer

This guide will help you deploy your WhatsApp Chat Analyzer app to various platforms.

## Recommended Platform: Streamlit Cloud

### Why Streamlit Cloud?
- Designed specifically for Streamlit apps
- Handles file uploads correctly
- Free tier available
- Easy GitHub integration
- No server configuration needed

### How to Deploy to Streamlit Cloud

1. Make sure your code is in a GitHub repository.

2. Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.

3. Select your repository, branch, and main file (`app.py`).

4. Deploy! Streamlit Cloud will automatically install dependencies from your `requirements.txt`.

5. Your app will be available at `https://[your-app-name].streamlit.app`

### Important Notes for Streamlit Cloud
- The file uploader widget in Streamlit handles files correctly by default
- Session state works properly
- No need to modify any server configurations

## Alternative: Heroku Deployment

1. Make sure you have the Heroku CLI installed.

2. Login to Heroku and create a new app:
   ```
   heroku login
   heroku create your-app-name
   ```

3. Push your code to Heroku:
   ```
   git push heroku main
   ```

4. Open your app:
   ```
   heroku open
   ```

### Important Notes for Heroku
- Set the stack to container if needed: `heroku stack:set container`
- You may need to add buildpacks: `heroku buildpacks:add heroku/python`
- The Procfile and setup.sh files are essential for Heroku deployment

## Alternative: Render Deployment

1. Sign up at [render.com](https://render.com/)

2. Connect your GitHub repository

3. Create a new Web Service with these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py`
   - Select the appropriate Python version

4. Deploy!

## Troubleshooting Deployment Issues

### File Access Problems
- If file uploads still fail, check that temporary files are being created and read correctly
- Ensure your app has proper permissions to create and read files
- Use the session state to store processed data rather than relying on file system

### Time Comparison Button Not Working
- Check browser console for JavaScript errors
- Ensure all dependencies are properly installed
- Verify that date comparisons are working with the correct date formats

### General Issues
- Check application logs on your deployment platform
- Ensure all required dependencies are in requirements.txt
- For NLTK or spaCy resources, ensure they're downloaded in the setup.sh script

## Testing Your Deployment

1. Try uploading small WhatsApp chat files first
2. Test different analysis types one by one
3. Check that the Time Comparison feature works with different date ranges

## Need More Help?

If you continue to experience deployment issues, please:
1. Check the logs on your deployment platform
2. Ensure all files mentioned in this guide are correctly configured
3. Consider adding more detailed error reporting in your app to pinpoint issues 