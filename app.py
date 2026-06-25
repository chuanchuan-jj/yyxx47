from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
import numpy as np

app = Flask(__name__)
CORS(app)

wine = load_wine()
X = wine.data
y_true = wine.target
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/cluster', methods=['GET'])
def get_cluster():
    eps = float(request.args.get('eps', 2.5))
    min_samples = int(request.args.get('min_samples', 5))
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_scaled)
    ari = adjusted_rand_score(y_true, labels)
    nmi = normalized_mutual_info_score(y_true, labels)
    n_noise = int(np.sum(labels == -1))
    response_data = {
        'pca_points': X_pca.tolist(),  
        'cluster_labels': labels.tolist(),
        'ari': round(ari, 4),
        'nmi': round(nmi, 4),
        'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
        'n_noise': n_noise
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)