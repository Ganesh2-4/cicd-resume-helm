from flask import Flask, render_template
import yaml, os
app = Flask(__name__, template_folder='templates', static_folder='static')

def load_resume(path='resume.yml'):
    if not os.path.exists(path):
        return {'error':'resume.yml not found'}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@app.route('/')
def index():
    resume = load_resume(os.path.join(app.root_path, 'resume.yml'))
    return render_template('index.html', resume=resume)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
