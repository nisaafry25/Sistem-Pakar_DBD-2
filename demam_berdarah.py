from flask import Flask, session, redirect, url_for, render_template, request

app = Flask(__name__)
app.secret_key = 'isinya password buat session'
app.static_folder = 'static'

# Daftar gejala demam berdarah
daftarGejala = [
    'Demam tinggi mendadak',
    'Sakit kepala parah',
    'Nyeri di belakang mata',
    'Nyeri sendi dan otot',
    'Mual dan muntah',
    'Kelelahan',
    'Ruam kulit',
    'Pendarahan ringan (gusi berdarah, mimisan)'
]

# Hanya satu penyakit dalam konteks ini, tapi bisa dikembangkan
daftarPenyakit = [
    'Demam Berdarah Dengue'
]

# Solusi untuk demam berdarah
solusiPenyakit = [
    'Istirahat cukup, minum banyak cairan, obat penurun demam, dan konsultasi dengan dokter untuk penanganan lebih lanjut'
]

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    name = request.form.get('Name')
    session['namaPasien'] = name
    session['gejalaPasien'] = 0
    session['gejalaLog'] = []
    return redirect(url_for('diagnosa'))

@app.route('/diagnosa', methods=['POST', 'GET'])
def diagnosa():
    gejala_index = session.get('gejalaPasien', 0)
    
    if request.method == 'POST':
        pilihan = request.form.get('pilihan')
        if pilihan == 'ya':
            session['gejalaLog'].append(gejala_index)
        session['gejalaPasien'] = gejala_index + 1
        gejala_index = session['gejalaPasien']
    
    if gejala_index >= len(daftarGejala):
        return redirect(url_for('result'))

    pertanyaan = daftarGejala[gejala_index]
    name = session.get('namaPasien', 'Pasien')
    return render_template('diagnosa.html', pertanyaan=pertanyaan, name=name)

@app.route('/result')
def result():
    gejalaLog = session.get('gejalaLog', [])
    if len(gejalaLog) >= 4:  # contoh logika sederhana
        terjangkitPenyakit = daftarPenyakit[0]
        solusiPenyakitnya = solusiPenyakit[0]
    else:
        terjangkitPenyakit = "Kemungkinan tidak terkena demam berdarah."
        solusiPenyakitnya = "Tetap jaga kesehatan dengan pola hidup sehat dan waspada terhadap gejala yang mungkin timbul."

    return render_template("result.html", terjangkitPenyakit=terjangkitPenyakit, solusiPenyakitnya=solusiPenyakitnya, awal=url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
