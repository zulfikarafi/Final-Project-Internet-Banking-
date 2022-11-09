from asyncio.windows_events import NULL
import base64
import random
import time
from datetime import datetime, date
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import jwt
import datetime as dt

app = Flask(__name__)
cors_config = {
    "origins": ['http://127.0.0.1:5000/'],
    "methods": ['GET, POST, OPTIONS, PUT, PATCH, DELETE']
}

CORS(app, resources = {
    r"/*": cors_config
})


ctx = app.app_context()
ctx.push()



app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost:5432/Internet_Banking?sslmode=disable'
db = SQLAlchemy(app)
# CORS(app)
# CORS(app, supports_credentials=True)

class Nasabah(db.Model):
    id_nasabah = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True) 
    nik = db.Column(db.String(50), nullable=False, unique=True)
    nama = db.Column(db.String(50), nullable=False)
    # nama_belakang = db.Column(db.String(50), nullable=False)
    no_hp = db.Column(db.String(50), nullable=False, unique=True)
    pekerjaan = db.Column(db.String(50), nullable=False)
    # alamat = db.Column(db.String(250), nullable=False)
    # kota = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    
class Cabang(db.Model):
    id_cabang = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True) 
    regional = db.Column(db.String(50), nullable=False)
    nama = db.Column(db.String(50), nullable=False)
    alamat = db.Column(db.String(250), nullable=False)
    kota = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    

class Account(db.Model): 
    id_account = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True) 
    no_rekening = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Integer, nullable=True)                                            
    status = db.Column(db.String(50), nullable=True)
    jenis = db.Column(db.String(50), nullable=True)    
    id_nasabah = db.Column(db.Integer, db.ForeignKey('nasabah.id_nasabah'), nullable=True)
    id_cabang = db.Column(db.Integer, db.ForeignKey('cabang.id_cabang'), nullable=True)
    last_update = db.Column (db.DateTime, nullable=False)
    # transakasi_rel = db.relationship('Transaksi', backref='account')                                    #menghubungkan tabel akun dan transaksi, karena akan ada operasi antar saldo dan kolom tiap transaksi 
    
class Transaksi(db.Model):
    id_transaksi = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    waktu = db.Column (db.DateTime, nullable=False)                                                     # untuk mencatat waktu tiap melakukan transaksi
    saldo_masuk = db.Column(db.Integer, nullable=True)
    saldo_keluar = db.Column(db.Integer, nullable=True)                                                # merujuk saldo pada akun                       
    jenis_transaksi = db.Column(db.String(50), nullable=True)
    id_pengirim = db.Column(db.Integer, db.ForeignKey('account.id_account'), nullable=True)                               
    id_penerima = db.Column(db.Integer, db.ForeignKey('account.id_account'), nullable=True)
    
db.create_all() 
db.session.commit()


def auth_nasabah(auth):
    encode = base64.b64decode(auth[6:])
    str_encode = encode.decode('ascii')
    lst = str_encode.split(':')
    username = lst[0]
    password = lst[1]   
    nasabah = Nasabah.query.filter_by(username=username).filter_by(password=password).first()
    if nasabah:
        return (nasabah.id_nasabah)
    else:
        return 0 
    

def auth_cabang(auth):
    encode = base64.b64decode(auth[6:])
    str_encode = encode.decode('ascii')
    lst = str_encode.split(':')
    username = lst[0]
    password = lst[1]   
    cabang = Cabang.query.filter_by(username=username).filter_by(password=password).first()
    if cabang:
        return (cabang.id_cabang)
    else:
        return 0

# def auth_nasabah() :
#     # Masukkan dari Postman sudah di encode dengan Basic Auth, jadi harus di decode dulu untuk memisahkan username & password
#     pass_str = request.headers.get('Authorization')     
#     pass_bersih = pass_str.replace('Basic ',"")        
#     hasil_decode = base64.b64decode(pass_bersih)       
#     hasil_decode_bersih = hasil_decode.decode('utf-8')  
#     username_aja = hasil_decode_bersih.split(":")[0]    
#     pass_aja = hasil_decode_bersih.split(":")[1]

#     #Password yang sudah di decode dan dipisah dari username diatas di encode lagi
#     pass_encode = pass_aja.encode('utf-8')
#     pass_encode_2 = base64.b64encode(pass_encode)
#     pass_cek = pass_encode_2.decode('utf-8')
    
#     nasabah = Nasabah.query.filter_by(username=username_aja).filter_by(password=pass_cek).first_or_404()
#     if nasabah :
#     #Return silahkan sesuai kebutuhan
#         # return [user.user_id,user.is_admin]
#         return jsonify(username_aja,pass_cek)
#         # return (nasabah.id_nasabah)
#     else:
#         return 0

# def auth_cabang() :
#     # Masukkan dari Postman sudah di encode dengan Basic Auth, jadi harus di decode dulu untuk memisahkan username & password
#     pass_str = request.headers.get('Authorization')     
#     pass_bersih = pass_str.replace('Basic ',"")        
#     hasil_decode = base64.b64decode(pass_bersih)       
#     hasil_decode_bersih = hasil_decode.decode('utf-8')  
#     username_aja = hasil_decode_bersih.split(":")[0]    
#     pass_aja = hasil_decode_bersih.split(":")[1]

#     #Password yang sudah di decode dan dipisah dari username diatas di encode lagi
#     pass_encode = pass_aja.encode('utf-8')
#     pass_encode_2 = base64.b64encode(pass_encode)
#     pass_cek = pass_encode_2.decode('utf-8')
    
#     cabang = Cabang.query.filter_by(username=username_aja).filter_by(password=pass_cek).first_or_404()
#     if cabang :
#     #Return silahkan sesuai kebutuhan
#         # return [user.user_id,user.is_admin]
#         return jsonify(username_aja,pass_cek)
#         # return (cabang.id_cabang)
#     else:
#         return 0


# ----------------------------------------------------------------------------------------------->>> HOME (pingin buat login user or adm)
@app.route('/nasabah') 
def home_nasabah():
    return jsonify(
        "Selamat Datang di Bank Alltale"
    )


@app.route('/admin') 
def home_admin():
    return jsonify(
        "Selamat Datang di Bank Alltale"
    )


# ----------------------------------------------------------------------------------------------->>> NASABAH
@app.route('/nasabah/register', methods=['POST'])#by user
def create_nasabah():
    data = request.get_json()
    # akun = Account.query.filter_by(id_account=id).all()
    # encode_password_1 = data['password'].encode('utf-8')
    # encode_password_2 = base64.b64encode(encode_password_1)
    n = Nasabah( 
        nik = data['nik'],
        nama = data['nama'],
        no_hp = data['no_hp'],
        pekerjaan = data['pekerjaan'],
        username = data['username'],
        email = data['email'],
        password = data['password']
	)
    db.session.add(n)
    db.session.commit()
    nasabah = Nasabah.query.filter_by(nik=data['nik']).first()  #query berdasarkan isian(nik) utk mendapatkan id_nasabah
    a = Account(
        no_rekening = random.randint(100000, 500000),
        saldo = data['saldo'],
        jenis = data['jenis'],              
        status = "Aktif",                                                               
        id_cabang = data['id_cabang'],
        last_update = datetime.now(),
        id_nasabah = nasabah.id_nasabah 
    )
    try:                                    
        
        db.session.add(a)
        db.session.commit()
    except:
        return {
            "pesan": "data tidak tersimpan"
        }, 400   
    return {
        "pesan": "data tersimpan"
    }, 201
     
@app.route('/nasabah/update/<id>', methods=['PUT'])#by user
def update_nasabah(id):
    # decode = request.headers.get('Authorization')
    # allow = auth_cabang(decode)
    # auth = auth_nasabah()
    # encode_password_1 = data['password'].encode('utf-8')
    # encode_password_2 = base64.b64encode(encode_password_1)
    # allow = auth_nasabah(auth)
    # allow = auth_nasabah(decode)
    nasabah = Nasabah.query.filter_by(id_nasabah=id).first()   
    data  = request.get_json()

        # nasabah.nik = data['nik']
        # nasabah.nama = data['nama']
        # nasabah.no_hp = data['no_hp']
        # nasabah.pekerjaan = data['pekerjaan']
        # nasabah.username = data['username']
        # nasabah.email = data['email']
        # nasabah.password = data['password']
    # nasabah.nik = data['nik']
    # nasabah.nama = data['nama']
    nasabah.no_hp = data['no_hp']
    nasabah.pekerjaan = data['pekerjaan']
    # nasabah.username = data['username']
    nasabah.email = data['email']
    # nasabah.password = data['password']

    db.session.commit()
    return {
        "pesan": "data telah tersimpan"
        }, 201

@app.route('/nasabah/update/password/<id>', methods=['PUT'])#by user
def update_nasabah_password(id):
    # decode = request.headers.get('Authorization')
    # allow = auth_cabang(decode)
    # auth = auth_nasabah()
    # encode_password_1 = data['password'].encode('utf-8')
    # encode_password_2 = base64.b64encode(encode_password_1)
    # allow = auth_nasabah(auth)
    # allow = auth_nasabah(decode)
    nasabah = Nasabah.query.filter_by(id_nasabah=id).first()   
    data  = request.get_json()

        # nasabah.nik = data['nik']
        # nasabah.nama = data['nama']
        # nasabah.no_hp = data['no_hp']
        # nasabah.pekerjaan = data['pekerjaan']
        # nasabah.username = data['username']
        # nasabah.email = data['email']
        # nasabah.password = data['password']
    # nasabah.nik = data['nik']
    # nasabah.nama = data['nama']
    # nasabah.no_hp = data['no_hp']
    # nasabah.pekerjaan = data['pekerjaan']
    # # nasabah.username = data['username']
    # nasabah.email = data['email']
    nasabah.password = data['password']

    db.session.commit()
    return {
        "pesan": "data telah tersimpan"
        }, 201

@app.route('/nasabah/profile/<id>', methods=['GET'])#by user
def profile_nasabah(id):
    # decode = request.headers.get('Authorization')
    # allow = auth_cabang(decode)
    # allow = auth_nasabah(auth)
    # allow = auth_nasabah(decode)
    nasabah = Nasabah.query.filter_by(id_nasabah=id).all()
    arr = []
    for i in nasabah:
        arr.append({
            "nik" : i.nik,
            "nama" : i.nama,
            "no_hp" : i.no_hp,
            "pekerjaan" : i.pekerjaan,
            "username" : i.username,
            "email" : i.email,
            "password" : i.password
        }
    )
    return (arr)
#     nasabah = Nasabah.query.filter_by(id_nasabah=id).first()
#     return jsonify({
#         "nik" : nasabah.nik,
#         "nama" : nasabah.nama,
#         "no_hp" : nasabah.no_hp,
#         "pekerjaan" : nasabah.pekerjaan,
#         "username" : nasabah.username,
#         "email" : nasabah.email,
#         "password" : nasabah.password
#     }
# )
#cara pake auth
# @app.route('/nasabah/profile/, methods=['GET'])#by user
# def profile_nasabah(:
#     decode = request.headers.get('Authorization')
#     allow = auth_nasabah(decode)
#     # allow = auth_nasabah(auth)
#     # allow = auth_nasabah(decode)
#     nasabah = Nasabah.query.filter_by(id_nasabah=allow).all()
#     if not allow :
#         return {
#                 "pesan" : "akses ditolak !!"
#             }, 400
#     else:
#         arr = []
#         nasabah = Nasabah.query.filter_by(id_nasabah=id_nasabah).all(
#         for i in nasabah:
#             arr.append({
#                 "nik" : i.nik,
#                 "nama" : i.nama,
#                 "no_hp" : i.no_hp,
#                 "pekerjaan" : i.pekerjaan,
#                 "username" : i.username,
#                 "email" : i.email,
#                 "password" : i.password
#             }
#         )
#         return (arr)    


# ----------------------------------------------------------------------------------------------->>> CABANG
@app.route('/cabang/register', methods=['POST']) #by admin
def create_cabang():
    data = request.get_json()
    # encode_password_1 = data['password'].encode('utf-8')
    # encode_password_2 = base64.b64encode(encode_password_1)
    c = Cabang( 
        
        regional = data['regional'],
        nama = data['nama'],
        alamat = data['alamat'],
        kota = data['kota'],
        username = data['username'],
        email = data['email'],
        password = data['password']
        # encode_password_2.decode('utf-8')
	)
    try:                                    
        db.session.add(c)
        db.session.commit()
    except:
        return {
            "pesan": "data tidak tersimpan"
        }, 400   
    return {
        "pesan": "data tersimpan"
    }, 201

@app.route('/cabang/profile', methods=['GET']) #by admin
def get_cabang_login():
    decode = request.headers.get('Authorization')
    allow = auth_cabang(decode)
    cabang = Cabang.query.filter_by(id_cabang=allow).first()
    if not allow :
        return {
                "pesan" : "akses ditolak !!"
            }, 400
    else:
        return jsonify([{
                "regional" : cabang.regional,
                "nama" : cabang.nama,
                "alamat" : cabang.alamat,
                "kota" : cabang.kota
            }]), 201

@app.route('/cabang', methods=['GET']) #by admin
def get_cabang():
    # decode = request.headers.get('Authorization')
    # allow = auth_cabang(decode)
    cabang = db.engine.execute(f'''SELECT distinct * FROM public.cabang ORDER BY id_cabang ASC ''')
    arr = []
    for i in cabang:
        arr.append({
            "id_cabang" : i[0],   
            "nama" : i[2]
            
        })
    return jsonify(arr)
        
@app.route('/cabang/update', methods=['PUT']) #by admin
def update_cabang():
    decode = request.headers.get('Authorization')
    allow = auth_nasabah(decode)
    cabang = Cabang.query.filter_by(id_cabang=allow).first()
    if not cabang :
        return {
            'pesan': 'data gagal tersimpan'
        }, 400
    else:
        data  = request.get_json()
        cabang = Cabang.query.filter_by(id_cabang=id).first()
        cabang.regional = data['regional']
        cabang.nama = data['nama']
        cabang.alamat = data['alamat']
        cabang.kota = data['kota']
        return {
            "pesan": "data telah tersimpan"
            }, 201

# @app.route('/cabang/total', methods=['GET'])
# def jumlah_account():
#     decode = request.headers.get('Authorization')
#     allow = auth_cabang(decode)
#     cabang = Cabang.query.filter_by(id_cabang=allow).first()
#     if not cabang :
#         return {
#             'pesan': 'Akses Ditolak !!'
#         }, 400
#     else:
#         total = db.engine.execute("select count(account.id_account), count(distinct(account.id_nasabah)), sum(account.saldo) from account inner join cabang on account.id_cabang = cabang.id_cabang")
#         arr = []
#         for i in total:
#             arr.append (
#                 {
#                     'total_account' : i[0],
#                     'total_nasabah' : i[1],
#                     'Jumlah_saldo' : i[2]
                    
#                 }), 201
#         return jsonify(arr)

@app.route('/cabang/total/<id>', methods=['GET'])
def jumlah_account(id):
    # cabang = Cabang.query.filter_by(id_cabang=id).first()
    total = db.engine.execute('select count(account.id_account), count(distinct(account.id_nasabah)), sum(account.saldo) from account inner join cabang on account.id_cabang = cabang.id_cabang where account.id_cabang = '+str(id)+'')
    arr = []
    for i in total:
        arr.append (
            {
                'total_account' : i[0],
                'total_nasabah' : i[1],
                'Jumlah_saldo' : i[2]
                
            }), 201
    return jsonify(arr)


@app.route('/cabang/total_percabang', methods=['GET'])
def jumlah_account_percabang():
    decode = request.headers.get('Authorization')
    allow = auth_cabang(decode)
    cabang = Cabang.query.filter_by(id_cabang=allow).first()
    if not cabang :
        return {
            'pesan': 'Akses Ditolak !!'
        }, 400
    else:
        total = db.engine.execute(f"select count(account.id_account), count(distinct(account.id_nasabah)), sum(account.saldo) from account inner join cabang on account.id_cabang = cabang.id_cabang where account.id_cabang = {allow}")
        arr = []
        for i in total:
            arr.append (
                {
                    'total_account' : i[0],
                    'total_nasabah' : i[1],
                    'Jumlah_saldo' : i[2]
                    
                }), 201
        return jsonify(arr)

@app.route('/cabang/transaksi_periode', methods=['GET'])
def jumlah_transaksi():
    decode = request.headers.get('Authorization')
    allow = auth_cabang(decode)
    cabang = Cabang.query.filter_by(id_cabang=allow).first()
    data = request.get_json()
    waktu = data["waktu"]
    waktu_2 = datetime.now()
    # waktu_2 = time.mktime(datetime.strptime(a,"%Y-%m-%d").timetuple())
    if not cabang :
        return {
            'pesan': 'Akses Ditolak !!'
        }, 400
    else:
        total = db.engine.execute(f"select  b.masuk, a.keluar, c.periode from (select sum(transaksi.saldo_keluar) as keluar from transaksi inner join account on transaksi.id_pengirim = account.id_account  inner join cabang on account.id_cabang = cabang.id_cabang where account.id_cabang = {allow})a,(select sum(transaksi.saldo_masuk) as masuk from transaksi inner join account on transaksi.id_penerima = account.id_account  inner join cabang on account.id_cabang = cabang.id_cabang where account.id_cabang = {allow})b, (select transaksi.waktu as periode from transaksi inner join account on transaksi.id_penerima = account.id_account  inner join cabang on account.id_cabang = cabang.id_cabang where waktu BETWEEN '2022-09-01' AND '{waktu_2}')c")
        arr = []
        for i in total:
            arr.append (
                {
                    'total_masuk' : i[0],
                    'total_keluar' : i[1],
                    'tanggal' : i[2]
                }), 201
        return jsonify(arr)

@app.route('/cabang/dorman', methods=['POST']) #by admin 
def get_dorman():
    decode = request.headers.get('Authorization')
    allow = auth_cabang(decode)
    cabang = Cabang.query.filter_by(id_cabang=allow).first()
    if not cabang :
            return {
                    "pesan" : "akses ditolak !!"
                }, 400
    else:
        data = request.get_json()
        no_account = data['id_account']
        arr = []
        len_ = []
        accounts = db.engine.execute(f"select distinct(waktu) from transaksi where id_pengirim= {no_account}")
        for i in accounts: 
            len_.append(i.waktu)
        for j in range(len(len_)-1):
            hasil = abs((len_[j] - len_[j+1]).days)
            akun = Account.query.filter_by(id_account=data['id_account']).first()
            if akun.status == "Tidak Aktif":
                return ({
                    'pesan' : "akun anda Tidak Aktif"
                    })
            if hasil > 90:
                arr.append({
                    'terakhir_transaksi' : len_[j],
                    'lama_dorman' : hasil,
                    'akun_Aktif_kembali' : len_[j+1]
                    })
                return arr
            else:
                return({
                    'pesan' : "tidak dorman"
                    # 'terakhir_transaksi' : len_[-1],
                    # 'lama_dorman' : 0
                    })
        else:
            return ({
                    'pesan' : "anda belum melakukan transaksi"
                    })

            
# @app.route('/nasabah/histori/<id>', methods=['GET']) #by admin 
# def get_histori_nasabah(id): 
#     # akun = Account.query.filter_by(id_nasabah=id).all()
#     pengirim = db.engine.execute('select b.id_transaksi, a.id_account, a.saldo, a.no_rekening, a.last_update, a.status, a.jenis, b.id_penerima, b.saldo_masuk, b.saldo_keluar, b.jenis_transaksi from account as a, transaksi as b where a.id_account = b.id_pengirim and a.id_nasabah= '+str(id)+'')
#     arr = []
    
#     for i in pengirim:
       
#         if i[7] == None:
#         #     arr.append({'Nama':"isinya null"})
#         # else:
#         #     arr.append({'Nama':"isinya ada"})
    
#     # return jsonify(arr)
#             arr.append({
#                     "penerima" : "",
#                     "saldo_keluar": i[9],
#                     "waktu" : i[4],
#                     "jenis_transaksi" : i[10],
#                     "no_rekening" : i[3],
#                     "id_transaksi" : i[0]
#                 })
#         else:
#             yang_menerima = db.engine.execute('SELECT DISTINCT * FROM account WHERE id_account='+str(i[1])+'')
#             for j in yang_menerima:
#                 nasabah = Nasabah.query.filter_by(id_nasabah=j[6]).first()
#                 arr.append({
#                 "penerima" : nasabah.nama,
#                 "saldo_keluar": i[9],
#                 "waktu" : i[4],
#                 "jenis_transaksi" : i[10],
#                 "no_rekening" : i[3],
#                 "id_transaksi" : i[0]
#             })

#     penerima = db.engine.execute('select b.id_transaksi, a.id_account, a.saldo, a.no_rekening, a.last_update, a.status, a.jenis, b.id_pengirim, b.saldo_masuk, b.saldo_keluar, b.jenis_transaksi from account as a, transaksi as b where a.id_account = b.id_pengirim and a.id_nasabah= '+str(id)+'')
    
#     for i in penerima:
       
#         if i[7] == None:
#         #     arr.append({'Nama':"isinya null"})
#         # else:
#         #     arr.append({'Nama':"isinya ada"})
    
#     # return jsonify(arr)
#             arr.append({
#                     "pengirim" : "",
#                     "saldo_masuk": i[8],
#                     "waktu" : i[4],
#                     "jenis_transaksi" : i[10],
#                     "no_rekening" : i[3],
#                     "id_transaksi" : i[0]
#                 })
#         else:
#             yang_ngirim = db.engine.execute('SELECT DISTINCT * FROM account WHERE id_account='+str(i[1])+'')
#             for j in yang_ngirim:
#                 nasabah = Nasabah.query.filter_by(id_nasabah=j[6]).first()
#                 arr.append({
#                 "pengirim" : nasabah.nama,
#                 "saldo_masuk": i[9],
#                 "waktu" : i[4],
#                 "jenis_transaksi" : i[10],
#                 "no_rekening" : i[3],
#                 "id_transaksi" : i[0]
#             })
#        #untuk penerima
       
#     #     arr.append({
#     #         "penerima" : nasabah.nama,
#     #         "saldo_keluar": i[9],
#     #         "waktu" : i[4],
#     #         "jenis_transaksi" : i[10]
#     #     })
#     return jsonify(arr)

@app.route('/nasabah/histori/<id>', methods=['GET']) #by admin 
def get_histori_nasabah(id): 
    # akun = Account.query.filter_by(id_nasabah=id).all()
    pengirim = db.engine.execute('select distinct y.no_rekening, z.nama, x.waktu, x.saldo_keluar, x.saldo_masuk, x.jenis_transaksi from transaksi as x join account as y on x.id_pengirim = y.id_account join nasabah as z on y.id_nasabah = z.id_nasabah where z.id_nasabah = '+str(id)+'order by x.waktu')
    
    penerima = db.engine.execute('select distinct y.no_rekening, z.nama, x.waktu, x.saldo_keluar, x.saldo_masuk, x.jenis_transaksi from transaksi as x join account as y on x.id_penerima = y.id_account join nasabah as z on y.id_nasabah = z.id_nasabah  where z.id_nasabah = '+str(id)+'order by x.waktu')
    arr = []
    
    for i in pengirim:
        arr.append({
                "nama" : i[1],
                "status" : 'pengirim',
                "saldo_masuk": i[4],
                "saldo_keluar": i[3],
                "waktu" : i[2],
                "jenis_transaksi" : i[5],
                "no_rekening" : i[0],    
            })
    for j in penerima:
        arr.append({
                "nama" : j[1],
                "status" : 'penerima',
                "saldo_masuk": j[4],
                "saldo_keluar": j[3],
                "waktu" : j[2],
                "jenis_transaksi" : j[5],
                "no_rekening" : j[0],    
            })

       #untuk penerima
       
    #     arr.append({
    #         "penerima" : nasabah.nama,
    #         "saldo_keluar": i[9],
    #         "waktu" : i[4],
    #         "jenis_transaksi" : i[10]
    #     })
    return jsonify(arr)

          

@app.route('/cabang/nasabah', methods=['GET']) #by admin 
def get_nasabah():
    decode = request.headers.get('Authorization')
    allow = auth_cabang(decode)
    # cabang = Cabang.query.filter_by(id_cabang=allow).filter_by(id_).first()
    if not allow :
            return {
                    "pesan" : "akses ditolak !!"
                }, 400
    else:
        
        nasabah_ = db.engine.execute(f"select id_nasabah from account where id_cabang = {allow} group by id_nasabah")
        arr = []
        for i in nasabah_:
            a = Nasabah.query.filter_by(id_nasabah=i.id_nasabah).first()
            arr.append({
                'nama' : a.nama,
                'email' : a.email
            })
        return jsonify(arr)



# ----------------------------------------------------------------------------------------------->>> ACCOUNT
# @app.route('/create_account_nasabah', methods=['POST']) #by admin 
# def create_account():
#     decode = request.headers.get('Authorization')
#     allow = auth_cabang(decode)
#     cabang = Cabang.query.filter_by(id_cabang=allow).first()
#     if not cabang :
#         return {
#             'pesan': 'Akses Ditolak !!'
#         }, 400
#     else:
#         data = request.get_json()
#         a = Account( 
#             no_rekening = random.randint(100000, 500000) + data["id_nasabah"],              #random.randint (u/ mengambil angka secara acak range dari 100000-500000) + data u/ menambahkan id agar tidak sama 
#             saldo = data['saldo'],
#             status = "Aktif",                                                               #awal membuat akun
#             jenis = data['jenis'],
#             id_nasabah = data['id_nasabah'],
#             id_cabang = data['id_cabang'],
#             last_update = datetime.now()                                                    # fungsi mengambil waktu saat itu
#         )
                                    
#         db.session.add(a)                                                                   # menambah data ke column
#         db.session.commit()                                                                 # menambah data ke database
#         acc = db.engine.execute("select * from account order by id_account  DESC limit 1")  # select data mysql
#         # new_account = []
#         # for x in  acc:                                                                       
#         #     new_account.append({'id_account': x[0], 'no_rekening': x[1], 'saldo' : x[2], 'status' : x[3], 'last_update': x[4], 'id_nasabah' : x[5], 'id_cabang' : x[6]}),201 
#         # return new_account
#         ### yang diatas untuk looping apabila lebih dari satu tabel contohnya join
#         for x in  acc:                                                                      # looping data dalam baris pada tabel akun (tidak ditambah list kosong karena hanya satu tabel 
#             return({'id_account': x[0], 'no_rekening': x[1], 'saldo' : x[2], 'status' : x[3], 'last_update': x[4], 'jenis' : x[5], 'id_nasabah' : x[6], 'id_cabang' : x[7]}),201 # untuk menampilkan baris baru yang ditambahkan pada tabel akun 
   
@app.route('/create_account_nasabah/<id>', methods=['POST']) #by admin 
def create_account(id):
    nasabah = Nasabah.query.filter_by(id_nasabah=id).first()
    
    data = request.get_json()
    a = Account( 
        no_rekening = random.randint(100000, 500000),              #random.randint (u/ mengambil angka secara acak range dari 100000-500000) + data u/ menambahkan id agar tidak sama 
        saldo = data['saldo'],
        status = "Aktif",                                                               #awal membuat akun
        jenis = data['jenis'],
        id_nasabah = nasabah.id_nasabah,
        id_cabang = data['id_cabang'],
        last_update = datetime.now()
                                                           # fungsi mengambil waktu saat itu
    )
                                
    try:                                    
        
        db.session.add(a)
        db.session.commit()
    except:
        return {
            "pesan": "data tidak tersimpan"
        }, 400   
    return {
        "pesan": "data tersimpan"
    }, 201
   

@app.route('/account/profile/<id>', methods=['GET']) #by user
def get_account(id):
    # decode = request.headers.get('Authorization')
    # nasabah_id = auth_nasabah(decode)                            #auth dari nasabah

    accounts = Account.query.filter_by(id_nasabah=id).all() #merujuk pada username dan password nasabah
    arr = []
    arr2 = []
    for i in accounts :
        arr.append(i.no_rekening)
        
    for j in arr :
        dorman = Account.query.filter_by(no_rekening=j).first()
        days_off = datetime.now() - dorman.last_update
        if days_off.days > 90 :
            arr2.append({
            "id_account" : dorman.id_account,
            "saldo" : dorman.saldo,
            "status" : "Tidak Aktif",
            "jenis" : dorman.jenis,
            "id_nasabah" : dorman.id_nasabah,
            "no_rekening" : dorman.no_rekening
            })
            dorman.status = "Tidak Aktif"                           #untuk update di db
        else:
            if dorman.status != "Tidak Aktif":
                arr2.append({
                "id_account" : dorman.id_account,
                "saldo" : dorman.saldo,
                "status" : "Aktif",
                "jenis" : dorman.jenis,
                'id_nasabah' : dorman.id_nasabah,
                "no_rekening" : dorman.no_rekening
                })
            
                
    db.session.commit()  
    accounts = Account.query.filter_by(id_nasabah=id).all()
    arr3 =[]
    for k in accounts:
        arr3.append({"no_rekening" : k.no_rekening, "id_account" : k.id_account, "saldo" : k.saldo, "status" : k.status,"jenis":k.jenis})               
    return jsonify(arr3) 
                                             
# @app.route('/account/deactivate/<id>', methods=['PUT']) #by admin
# def deactivate_account(id):
#     decode = request.headers.get('Authorization')
#     cabang = auth_cabang(decode)
#     if cabang :
#         account_id = Account.query.filter_by(id_account=id).first()
#         if account_id :
#             account_id.status = "Tidak Aktif"
#         db.session.commit()  
#         return { 
#             "pesan" : "akun anda telah non Aktif"
#         },201
#     return { 
#             "pesan" : "password atau username anda salah"
#         },400
    
@app.route('/account/deactivate/<id>', methods=['PUT']) #by admin
def deactivate_account(id):
    # nasabah = Nasabah.query.filter_by(id_nasabah=id).first()
    akun= Account.query.filter_by(id_account=id).first()
    # return akun.status
    if akun :
        akun.status = "Tidak Aktif"
        db.session.commit()  
        return { 
            "pesan" : "akun anda telah non Aktif"
        },201



@app.route('/account/reactivate/<id>', methods=['PUT'])#by admin
def reactivate_account(id):
    decode = request.headers.get('Authorization')
    cabang = auth_cabang(decode)
    if cabang :
        account_id = Account.query.filter_by(id_account=id).first()
        if account_id :
            account_id.status = "Aktif"
            account_id.last_update = datetime.now()
            db.session.commit()  
        return { 
            "pesan" : "akun anda telah Aktif"
        },201
    return { 
            "pesan" : "password atau username anda salah"
        },400    
    


# ----------------------------------------------------------------------------------------------->>> TRANSAKSI 
# @app.route('/transaksi/transfer', methods=['POST']) #by user
# def transaksi_transfer():
#     decode = request.headers.get('Authorization')
#     id_nasabah = auth_nasabah(decode)
#     if id_nasabah :
#         data = request.get_json()
#         pengirim = Account.query.filter_by(id_account=data['id_pengirim']).filter_by(id_nasabah=id_nasabah).first() 
#         if not pengirim :
#             return {
#                     "pesan" : "akses ditolak !!"
#                 }, 400
#         penerima = Account.query.filter_by(id_account=data['id_penerima']).first() 
#         day_off = datetime.now() - pengirim.last_update
#         no_activity = day_off.days   
#         if no_activity > 90 or penerima.status != "Aktif" or pengirim.status != "Aktif":
#             return {
#                     "pesan" : "akun anda Tidak Aktif"
#                 }, 400
#         else :
#             if pengirim.jenis == "PLATINUM":
#                 if data['saldo_keluar'] <= 25000000:
#                     if pengirim.saldo - data['saldo_keluar'] > 50000 :
#                         pengirim.saldo = pengirim.saldo - data['saldo_keluar']
#                         pengirim.last_update == datetime.now()
#                         saldosebelum = pengirim.saldo + data['saldo_keluar']
#                         t = Transaksi( 
#                             waktu = datetime.now(),
#                             saldo_masuk = data['saldo_keluar'],
#                             saldo_keluar = data['saldo_keluar'],
#                             jenis_transaksi = "Transfer",
#                             id_pengirim = data['id_pengirim'],              
#                             id_penerima = data['id_penerima']
                                       
#                                     )
#                         penerima.saldo = penerima.saldo + data['saldo_keluar']
#                         db.session.add(t)
#                         db.session.commit()
#                         return { 
#                             "waktu" : datetime.now(),
#                             "saldo_sebelum" : saldosebelum,
#                             "saldo_setelah" : pengirim.saldo,                                                    
#                             "transfer" : data['saldo_keluar']
#                         }, 201
#                     else:
#                         return {
#                             "pesan": "saldo anda tidak cukup"
#                         }, 400
#                 else:
#                     return {
#                             "pesan": "anda melebihi maksimum"
#                         }, 400
                        
#             if pengirim.jenis == "GOLD":
#                 if data['saldo_keluar'] <= 50000000:
#                     if pengirim.saldo - data['saldo_keluar'] > 50000 :
#                         pengirim.saldo = pengirim.saldo - data['saldo_keluar']
#                         pengirim.last_update == datetime.now()
#                         saldosebelum = pengirim.saldo + data['saldo_keluar']
#                         t = Transaksi( 
#                             waktu = datetime.now(),
#                             saldo_masuk = data['saldo_keluar'],
#                             saldo_keluar = data['saldo_keluar'],
#                             jenis_transaksi = "Transfer",
#                             id_pengirim = data['id_pengirim'],              
#                             id_penerima = data['id_penerima']               
#                                     )
#                         penerima.saldo = penerima.saldo + data['saldo_keluar']
#                         db.session.add(t)
#                         db.session.commit()
#                         return { 
#                             "waktu" :  datetime.now(),
#                             "saldo_sebelum" : saldosebelum,
#                             "saldo_setelah" : pengirim.saldo,                                                    
#                             "transfer" : data['saldo_keluar']
#                         }, 201
#                     else:
#                         return {
#                             "pesan": "saldo anda tidak cukup"
#                         }, 400
#                 else:
#                     return {
#                             "pesan": "anda melebihi maksimum"
#                         }, 400

#             if pengirim.jenis == "BLACK":
#                 if data['saldo_keluar'] <= 100000000:
#                     if pengirim.saldo - data['saldo_keluar'] > 50000 :
#                         pengirim.saldo = pengirim.saldo - data['saldo_keluar']
#                         pengirim.last_update == datetime.now()
#                         saldosebelum = pengirim.saldo + data['saldo_keluar']
#                         t = Transaksi( 
#                             waktu = datetime.now(),
#                             saldo_masuk = data['saldo_keluar'],
#                             saldo_keluar = data['saldo_keluar'],
#                             jenis_transaksi = "Transfer",
#                             id_pengirim = data['id_pengirim'],              
#                             id_penerima = data['id_penerima']               
#                                     )
#                         penerima.saldo = penerima.saldo + data['saldo_keluar'] 
#                         db.session.add(t)
#                         db.session.commit()
#                         return { 
#                             "waktu" :  datetime.now(),
#                             "saldo_sebelum" : saldosebelum,
#                             "saldo_setelah" : pengirim.saldo,                                                    
#                             "transfer" : data['saldo_keluar']
#                         }, 201
#                     else:
#                         return {
#                             "pesan": "saldo anda tidak cukup"
#                         }, 400
#                 else:
#                     return {
#                             "pesan": "anda melebihi maksimum"
#                         }, 400                  
#     else :
#         return {
#             'pesan': 'Akses Ditolak !!'
#         }, 400

@app.route('/transaksi/transfer/<id>', methods=['POST']) #by user
def transaksi_transfer(id):
    # decode = request.headers.get('Authorization')
    # id_nasabah = auth_nasabah(decode)
    data = request.get_json()
    pengirim = Account.query.filter_by(no_rekening=str(data['norek_pengirim'])).filter_by(id_nasabah=id).first_or_404()
    # pengirim = Account.query.filter_by(id_account=id).first()
    penerima = Account.query.filter_by(no_rekening=str(data['norek_penerima'])).first() 
    day_off = datetime.now() - pengirim.last_update
    no_activity = day_off.days   
    if no_activity > 90 or penerima.status != "Aktif" or pengirim.status != "Aktif":
        return {
                "pesan" : "akun anda Tidak Aktif"
            }, 400
    else :
        if pengirim.jenis == "PLATINUM":
            if data['saldo_keluar'] <= 25000000:
                if pengirim.saldo - data['saldo_keluar'] > 50000 :
                    pengirim.saldo = pengirim.saldo - data['saldo_keluar']
                    pengirim.last_update == datetime.now()
                    saldosebelum = pengirim.saldo + data['saldo_keluar']
                    akun_pengirim = Account.query.filter_by(no_rekening=str(data["norek_pengirim"])).first()
                    akun_penerima = Account.query.filter_by(no_rekening=str(data["norek_penerima"])).first()
                    t = Transaksi( 
                        waktu = datetime.now(),
                        saldo_masuk = int(data['saldo_keluar']),
                        saldo_keluar = int(data['saldo_keluar']),
                        jenis_transaksi = "Transfer",
                        id_pengirim = akun_pengirim.id_account,              
                        id_penerima = akun_penerima.id_account 
                                    
                                )
                    penerima.saldo = penerima.saldo + data['saldo_keluar']
                    db.session.add(t)
                    db.session.commit()
                    return { 
                        "waktu" : datetime.now(),
                        "saldo_sebelum" : saldosebelum,
                        "saldo_setelah" : pengirim.saldo,                                                    
                        "transfer" : data['saldo_keluar'],
                        "pesan" : "berhasil"
                    }, 201
                else:
                    return {
                        "pesan": "saldo anda tidak cukup"
                    }, 400
            else:
                return {
                        "pesan": "anda melebihi maksimum"
                    }, 400
                    
        if pengirim.jenis == "GOLD":
            if data['saldo_keluar'] <= 50000000:
                if pengirim.saldo - data['saldo_keluar'] > 50000 :
                    pengirim.saldo = pengirim.saldo - data['saldo_keluar']
                    pengirim.last_update == datetime.now()
                    saldosebelum = pengirim.saldo + data['saldo_keluar']
                    akun_pengirim = Account.query.filter_by(no_rekening=str(data["norek_pengirim"])).first()
                    akun_penerima = Account.query.filter_by(no_rekening=str(data["norek_penerima"])).first()
                    t = Transaksi( 
                        waktu = datetime.now(),
                        saldo_masuk = int(data['saldo_keluar']),
                        saldo_keluar = int(data['saldo_keluar']),
                        jenis_transaksi = "Transfer",
                        id_pengirim = akun_pengirim.id_account,              
                        id_penerima = akun_penerima.id_account               
                                )
                    penerima.saldo = penerima.saldo + data['saldo_keluar']
                    db.session.add(t)
                    db.session.commit()
                    return { 
                        "waktu" :  datetime.now(),
                        "saldo_sebelum" : saldosebelum,
                        "saldo_setelah" : pengirim.saldo,                                                    
                        "transfer" : data['saldo_keluar'],
                        "pesan" : "berhasil"
                    }, 201
                else:
                    return {
                        "pesan": "saldo anda tidak cukup"
                    }, 400
            else:
                return {
                        "pesan": "anda melebihi maksimum"
                    }, 400

        if pengirim.jenis == "BLACK":
            if data['saldo_keluar'] <= 100000000:
                if pengirim.saldo - data['saldo_keluar'] > 50000 :
                    pengirim.saldo = pengirim.saldo - data['saldo_keluar']
                    pengirim.last_update == datetime.now()
                    saldosebelum = pengirim.saldo + data['saldo_keluar']
                    akun_pengirim = Account.query.filter_by(no_rekening=str(data["norek_pengirim"])).first()
                    akun_penerima = Account.query.filter_by(no_rekening=str(data["norek_penerima"])).first()
                    t = Transaksi( 
                        waktu = datetime.now(),
                        saldo_masuk = int(data['saldo_keluar']),
                        saldo_keluar = int(data['saldo_keluar']),
                        jenis_transaksi = "Transfer",
                        id_pengirim = akun_pengirim.id_account,              
                        id_penerima = akun_penerima.id_account           
                                )
                    penerima.saldo = penerima.saldo + data['saldo_keluar'] 
                    db.session.add(t)
                    db.session.commit()
                    return { 
                        "waktu" :  datetime.now(),
                        "saldo_sebelum" : saldosebelum,
                        "saldo_setelah" : pengirim.saldo,                                                    
                        "transfer" : data['saldo_keluar'],
                        "pesan" : "berhasil"
                    }, 201
                else:
                    return {
                        "pesan": "saldo anda tidak cukup"
                    }, 400
            else:
                return {
                        "pesan": "anda melebihi maksimum"
                    }, 400                  



# @app.route('/cabang/transaksi/setor_tunai', methods=['POST']) #by admin
# def transaksi_setor_tunai():
#     decode = request.headers.get('Authorization')
#     allow = auth_cabang(decode)
#     cabang = Cabang.query.filter_by(id_cabang=allow).first()
#     if not cabang :
#         return {
#             'pesan': 'Akses Ditolak !!'
#         }, 400
#     else:
#         data = request.get_json()
#         penerima = Account.query.filter_by(id_account=data['id_penerima']).first()
#         day_off = datetime.now() - penerima.last_update
#         no_activity = day_off.days   
#         if no_activity > 90 :
#             penerima.status == "Tidak Aktif"
#             return {
#                     "pesan" : "akun Tidak Aktif"
#                 }, 400
#         else:
#             penerima.last_update == datetime.now()
#             # saldosebelum = penerima.saldo - data['saldo_masuk']
#             t = Transaksi( 
#                 waktu = datetime.now(),
#                 saldo_masuk = data['saldo_masuk'],
#                 saldo_keluar = 0,
#                 jenis_transaksi = "Setor Tunai",
#                 id_pengirim = data['id_penerima'],              
#                 id_penerima = data['id_penerima']               
#                 )
#             penerima.saldo = penerima.saldo + data['saldo_masuk']
#             db.session.add(t)
#             db.session.commit()
#             return { 
#                 "waktu" : datetime.now(),
#                 "setor_tunai" : data['saldo_masuk'],
#                 # "saldo_sebelum" : saldosebelum,                                                    
#                 "saldo_sesudah" : penerima.saldo
#             }, 201


@app.route('/cabang/transaksi/setor_tunai/<id>', methods=['POST']) #by admin
def transaksi_setor_tunai(id):
    data = request.get_json()
    penerima = Account.query.filter_by(no_rekening=str(data['norek_penerima'])).filter_by(id_nasabah=id).first_or_404() 
    day_off = datetime.now() - penerima.last_update
    no_activity = day_off.days   
    if no_activity > 90 :
        penerima.status == "Tidak Aktif"
        return {
                "pesan" : "akun Tidak Aktif"
            }, 400
    else:
        # penerima.last_update == datetime.now()
        # saldosebelum = penerima.saldo - data['saldo_masuk']
        t = Transaksi( 
            waktu = datetime.now(),
            saldo_masuk = data['saldo_masuk'],
            saldo_keluar = 0,
            jenis_transaksi = "Setor Tunai",
            # id_pengirim = data['id_penerima'],              
            id_penerima = penerima.id_account              
            )
        penerima.saldo = penerima.saldo + data['saldo_masuk']
        db.session.add(t)
        penerima.last_update = datetime.now()
        # db.session.add(a) 
        db.session.commit()
        return { 
            "waktu" : datetime.now(),
            "setor_tunai" : data['saldo_masuk'],
            # "saldo_sebelum" : saldosebelum,                                                    
            "saldo_sesudah" : penerima.saldo
        }, 201


@app.route('/transaksi/debit', methods=['POST']) #by user 
def transaksi_debit():
    decode = request.headers.get('Authorization')
    id_nasabah = auth_nasabah(decode)
    if id_nasabah :
        data = request.get_json()
        pengirim = Account.query.filter_by(id_account=data['id_pengirim']).filter_by(id_nasabah=id_nasabah).first() 
        if not pengirim :
            return {
                    "pesan" : "akses ditolak !!"
                }, 400       #query di postman 
        day_off = datetime.now() - pengirim.last_update
        no_activity = day_off.days   
        if no_activity > 90 :
            pengirim.status == "Tidak Aktif"
            return {
                    "pesan" : "akun anda Tidak Aktif"
                }, 400
        else :
            if pengirim.saldo - data['saldo_keluar'] > 50000 :
                pengirim.saldo = pengirim.saldo - data['saldo_keluar']
                pengirim.last_update == datetime.now()
                saldosebelum = pengirim.saldo + data['saldo_keluar']
                t = Transaksi( 
                    waktu = datetime.now(),
                    saldo_masuk = 0,
                    saldo_keluar = data['saldo_keluar'],
                    jenis_transaksi = "Debit",
                    id_pengirim = data['id_pengirim']             
                    # id_penerima = data['id_penerima']              
                        )
                db.session.add(t)
                db.session.commit()
                return { 
                    "waktu" : datetime.now(),
                    "saldo_sebelum" : saldosebelum,
                    "saldo_setelah" : pengirim.saldo,                                                    
                    "debit" : data['saldo_keluar']
                }, 201
            else:
                return {
                    "pesan": "saldo anda tidak cukup"
                }, 400
    else :
        return {
            'pesan': 'Akses Ditolak !!'
        }, 400

# @app.route('/transaksi/tarik_tunai', methods=['POST']) #by user 
# def transaksi_tarik_tunai():
#     decode = request.headers.get('Authorization')
#     id_nasabah = auth_nasabah(decode)
#     if id_nasabah :
#         data = request.get_json()
#         pengirim = Account.query.filter_by(id_account=data['id_pengirim']).filter_by(id_nasabah=id_nasabah).first() 
#         if not pengirim :
#             return {
#                     "pesan" : "akses ditolak !!"
#                 }, 400        
#         day_off = datetime.now() - pengirim.last_update
#         no_activity = day_off.days   
#         if no_activity > 90 :
#             pengirim.status == "Tidak Aktif"
#             return {
#                     "pesan" : "akun anda Tidak Aktif"
#                 }, 400
#         else :
#             if pengirim.saldo - data['saldo_keluar'] > 50000 :
#                 pengirim.saldo = pengirim.saldo - data['saldo_keluar']
#                 pengirim.last_update == datetime.now()
#                 saldosebelum = pengirim.saldo + data['saldo_keluar']
#                 t = Transaksi( 
#                     waktu = datetime.now(),
#                     saldo_masuk = 0,
#                     saldo_keluar = data['saldo_keluar'],
#                     jenis_transaksi = "Tarik Tunai",
#                     id_pengirim = data['id_pengirim'],              
#                     # id_penerima = data['id_penerima']               
#                         )
#                 db.session.add(t)
#                 db.session.commit()
#                 return { 
#                     "waktu" : datetime.now(),
#                     "saldo_sebelum" : saldosebelum,
#                     "saldo_setelah" : pengirim.saldo,                                                    
#                     "tarik_tunai" : data['saldo_keluar']
#                 }, 201
#             else:
#                 return {
#                     "pesan": "saldo anda tidak cukup"
#                 }, 400
#     else :
#         return {
#             'pesan': 'Akses Ditolak !!'
#         }, 400


@app.route('/transaksi/tarik_tunai/<id>', methods=['POST']) #by user 
def transaksi_tarik_tunai(id):
    data = request.get_json()
    pengirim = Account.query.filter_by(no_rekening=str(data['norek_pengirim'])).filter_by(id_nasabah=id).first_or_404() 
    # penerima = Account.query.filter_by(no_rekening=str(data['norek_penerima'])).first()      
    day_off = datetime.now() - pengirim.last_update
    no_activity = day_off.days   
    if no_activity > 90 :
        pengirim.status == "Tidak Aktif"
        return {
                "pesan" : "akun anda Tidak Aktif"
            }, 400
    else :
        if pengirim.saldo - data['saldo_keluar'] > 50000 :
            pengirim.saldo = pengirim.saldo - data['saldo_keluar']
            pengirim.last_update == datetime.now()
            saldosebelum = pengirim.saldo + data['saldo_keluar']
            akun_pengirim = Account.query.filter_by(no_rekening=str(data["norek_pengirim"])).first()
            # akun_penerima = Account.query.filter_by(no_rekening=str(data["norek_penerima"])).first()
            t = Transaksi( 
                waktu = datetime.now(),
                saldo_masuk = 0,
                saldo_keluar = data['saldo_keluar'],
                jenis_transaksi = "Tarik Tunai",
                id_pengirim = akun_pengirim.id_account            
                # id_penerima = akun_penerima.id_account
                              
                 )
            db.session.add(t)
            db.session.commit()
            return { 
                "waktu" : datetime.now(),
                "saldo_sebelum" : saldosebelum,
                "saldo_setelah" : pengirim.saldo,                                                    
                "tarik_tunai" : data['saldo_keluar']
            }, 201
        else:
            return {
                "pesan": "saldo anda tidak cukup"
            }, 400


#tes backend
# @app.route('/transaksi/tarik_tunai/<id>', methods=['POST']) #by user 
# def transaksi_tarik_tunai(id):
#     data = request.get_json()
#     a = data['norek_pengirim']
#     b =  data['saldo_keluar']

#     return jsonify(a,b) 
   



@app.route('/transaksi/history/<id>', methods=['GET']) #by user
def get_transaksi(id):
    # decode = request.headers.get('Authorization')
    # id_nasabah = auth_nasabah(decode)
    accounts = Account.query.filter_by(id_nasabah=id).all()
    arr = []
    arr2 = []
    
    # nasabah_pe = db.engine.execute('select a.id_penerima, b.id_account, c.id_nasabah, c.nama from transaksi as a, account as b, nasabah as c where a.id_penerima = b.id_account and c.id_nasabah= b.id_nasabah and a.id_penerima = 6')
    
    for i in accounts:
        transaksi = Transaksi.query.filter_by(id_pengirim=i.id_account).all()
        arr2.append(i.id_account)
        for j in transaksi:

            arr.append({
                    'waktu' : j.waktu,                                                    
                    'saldo_masuk' : j.saldo_masuk,
                    'saldo_keluar' : j.saldo_keluar,
                    'jenis_transaksi' : j.jenis_transaksi,
                    'id_pengirim' : j.id_pengirim,
                    'id_penerima' : j.id_penerima
                }  
    )
    # history menerima
    for i in accounts:
        transaksi = Transaksi.query.filter_by(id_penerima=i.id_account).all()
        arr2.append(i.id_account)
        for j in transaksi:
            arr.append({
                    'waktu' : j.waktu,                                                    
                    'saldo_masuk' : j.saldo_masuk,
                    'saldo_keluar' : j.saldo_keluar,
                    'jenis_transaksi' : j.jenis_transaksi,
                    'id_pengirim' : j.id_pengirim,
                    'id_penerima' : j.id_penerima
                }  
    )
    return arr

    
# ----------------------------------------------------------------------------------------------->>> Frontend

# ----------------------------------------------------------------------------------------------->>> NASABAH
@app.route('/login', methods=['POST']) #by user

def login():
    auth = request.headers.get('Authorization')
    allow = auth_nasabah(auth)
    data =Nasabah.query.filter_by(id_nasabah=allow).first()
    # if data: // untuk cek isi data
    #     return {"message": "true", "id": data.password}
    # else:
    #     return "false"
    if data:
        token = jwt.encode({
            'nama': data.nama,
            'usrname': data.username,
            'passkey' :data.password,
            'id': data.id_nasabah,
            'exp': datetime.now() + dt.timedelta(hours=24)},
            'secret' ,algorithm='HS256'
        )
        resp = make_response("token generated")
        resp.set_cookie('username', value=token,expires=datetime.now() + dt.timedelta(hours=24), path='/', samesite='Lax',)
        return {
            "pesan" : "sukses",
            "token" : token,
            "usrid" : data.id_nasabah
        }
    else:
        return "akses ditolak"
    
   
    
    
#     resp.set_cookie('token',value=token,expires=datetime.datetime.now() + datetime.timedelta(hours=24), path='/',samesite='Lax',)
#     resp.set_cookie('role',value=us.role,expires=datetime.datetime.now() + datetime.timedelta(hours=24), path='/',samesite='Lax',)
    

# ----------------------------------------------------------------------------------------------->>> ADMIN
@app.route('/login/admin', methods=['POST']) #by user

def login_admin():
    auth = request.headers.get('Authorization')
    allow = auth_cabang(auth)
    data = Cabang.query.filter_by(id_cabang=allow).first()
    # if data: // untuk cek isi data
    #     return {"message": "true", "id": data.password}
    # else:
    #     return "false"
    if data:
        token = jwt.encode({
            'nama': data.nama,
            'usrname': data.username,
            'passkey' :data.password,
            'id': data.id_cabang,
            'exp': datetime.now() + dt.timedelta(hours=24)},
            'secret' ,algorithm='HS256'
        )
        resp = make_response("token generated")
        resp.set_cookie('username', value=token,expires=datetime.now() + dt.timedelta(hours=24), path='/', samesite='Lax',)
        return {
            "pesan" : "sukses",
            "token" : token,
            "usrid" : data.id_cabang
        }
    else:
        return "akses ditolak"







# ----------------------------------------------------------------------------------------------->>> CORS
@app.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Accept, Authorization, Redirect')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    return response
