# ML VLAB

University gradient descent virtual laboratory, made by Riddhi Tamhankar and Niharika pawar.

## Open in VS Code

Open this folder. The site is buildless HTML, CSS and JavaScript in `dist/`.

```powershell
python -m http.server 5180 --directory dist
```

Visit http://localhost:5180. An HTTP server is required to load the CSV dataset.

## Edit

- `dist/index.html`: shared page structure and branding
- `dist/style.css`: academic theme and pink accent variables
- `dist/app.js`: seven sections, quizzes and gradient descent
- `dist/data/advertising.csv`: Kaggle Advertising dataset

Dataset source: https://www.kaggle.com/datasets/ashydv/advertising-dataset
KaTeX 0.16.22 is bundled locally under `dist/vendor/katex/`.

## Deploy from VS Code

In GitHub repository Settings → Pages, select **GitHub Actions** as the source.
The Deploy ML VLAB workflow publishes `dist/` on each push to `main`.
For the initial deployment after enabling Pages, open Actions → Deploy ML VLAB → Run workflow.

For later edits, use Source Control in VS Code: stage changes, enter a commit message,
commit, then Sync Changes. Or run:

```powershell
git add dist README.md .github
git commit -m "Update virtual lab"
git push origin main
```

The expected GitHub Pages address is https://riddhi200618.github.io/ML_VLAB/.
Check Actions for deployment completion before using that address.

## Checks

```powershell
node --check dist/app.js
node verify.cjs
node verify-design.cjs
```

The existing ChatGPT Sites publication is separate; GitHub pushes deploy to GitHub Pages.
