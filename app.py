from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import nmap
import socket
import pandas as pd
import plotly.express as px
import io

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Form doğrulaması için gerekli

def perform_scan(ip_range, ports, timeout):
    scanner = nmap.PortScanner()
    arguments = f"-sV -T4 --host-timeout {timeout}s"
    scanner.scan(ip_range, ports, arguments=arguments)
    
    devices = []
    for host in scanner.all_hosts():
        if scanner[host].state() == "up":
            hostname = socket.getfqdn(host)
            ports_found = []
            for proto in scanner[host].all_protocols():
                for port in scanner[host][proto]:
                    port_info = scanner[host][proto][port]
                    ports_found.append(f"{port} ({port_info.get('name','')})")
            devices.append({
                "IP": host,
                "Hostname": hostname,
                "Açık Port Sayısı": len(ports_found),
                "Açık Portlar": ", ".join(ports_found)
            })
    return devices

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ip_range = request.form.get("ip_range")
        ports = request.form.get("ports")
        timeout = request.form.get("timeout")
        if not ip_range or not ports or not timeout:
            flash("Tüm alanları doldurmanız gerekmektedir.", "danger")
            return redirect(url_for("index"))
        return redirect(url_for("scan", ip_range=ip_range, ports=ports, timeout=timeout))
    return render_template("index.html")

@app.route("/scan")
def scan():
    ip_range = request.args.get("ip_range")
    ports = request.args.get("ports")
    timeout = request.args.get("timeout", type=int)
    
    try:
        devices = perform_scan(ip_range, ports, timeout)
    except Exception as e:
        flash(f"Tarama sırasında bir hata oluştu: {e}", "danger")
        devices = []

    # DataFrame oluşturma
    df = pd.DataFrame(devices)
    # Plotly grafiği: Açık port sayısına göre dağılım
    if not df.empty:
        fig = px.histogram(df, x="Açık Port Sayısı", nbins=20, title="Cihazların Açık Port Sayısı Dağılımı")
        graph_html = fig.to_html(full_html=False)
    else:
        graph_html = None

    return render_template("results.html", devices=devices, graph_html=graph_html,
                           ip_range=ip_range, ports=ports, timeout=timeout)

@app.route("/download_csv")
def download_csv():
    ip_range = request.args.get("ip_range")
    ports = request.args.get("ports")
    timeout = request.args.get("timeout", type=int)
    devices = perform_scan(ip_range, ports, timeout)
    df = pd.DataFrame(devices)
    csv_buffer = io.StringIO()
    if not df.empty:
        df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return send_file(io.BytesIO(csv_buffer.getvalue().encode()),
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="netscan_results.csv")

if __name__ == "__main__":
    app.run(debug=True)
