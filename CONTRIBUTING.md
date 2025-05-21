# Contributing to WhatsApp Chat Analyzer

Thank you for your interest in contributing! Your help is welcome to make this project better for everyone.

## How to Contribute

1. **Fork the repository**
   - Click the "Fork" button at the top right of this repo page.
2. **Clone your fork**
   - `git clone https://github.com/YOUR-USERNAME/Whats_app_chat_analyzer.git`
3. **Create a new branch**
   - `git checkout -b feature/your-feature-name`
4. **Make your changes**
   - Add new features, fix bugs, improve docs, or refactor code.
5. **Test your changes**
   - Make sure the app runs: `streamlit run app.py`
   - Check for errors and test your feature.
6. **Commit and push**
   - `git add .`
   - `git commit -m "Describe your change"`
   - `git push origin feature/your-feature-name`
7. **Open a Pull Request**
   - Go to your fork on GitHub and click "New Pull Request".
   - Describe your changes and link any related issues.

## Contribution Guidelines

- Write clear, readable code and comments.
- Follow the existing code style (PEP8 for Python).
- Add docstrings to new functions or modules.
- Update or add documentation if needed.
- Be respectful and constructive in code reviews and discussions.

## Areas to Contribute

- New analysis features (e.g., more visualizations, new stats)
- UI/UX improvements
- Bug fixes
- Documentation improvements
- Support for more languages or chat formats
- Performance optimizations

## Reporting Issues

- Use the GitHub Issues tab to report bugs or request features.
- Please provide clear steps to reproduce bugs and screenshots if possible.

## Code of Conduct

Be kind, respectful, and inclusive. Harassment or discrimination will not be tolerated.

## Sample Contribution: Add a New Toxic Word

Suppose you want to add a new toxic word (e.g., "loser") to the toxicity detection:

1. Open `models/sentiment_toxicity.py`.
2. Find the `TOXIC_WORDS` set near the top.
3. Add your word to the set, e.g.:

   ```python
   TOXIC_WORDS = set([
       # ...existing words...
       'loser'
   ])
   ```

4. Save the file and run the app to test.
5. If it works, follow the steps above to commit and submit a pull request!

---

Thank you for helping make WhatsApp Chat Analyzer better!
