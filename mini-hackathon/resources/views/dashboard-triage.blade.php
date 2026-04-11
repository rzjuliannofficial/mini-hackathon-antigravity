@extends('layouts.app')

@section('content')
<div class="container-fluid mt-4">
    <div class="row mb-4">
        <div class="col-md-12">
            <h1 class="display-4">
                <i class="fas fa-heartbeat text-danger"></i> Emergency Monitor - Triage Dashboard
            </h1>
            <p class="text-muted">Monitoring real-time registrasi pasien darurat dari Antigravity AI System</p>
        </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card border-danger">
                <div class="card-body text-center">
                    <h5 class="card-title">🔴 MERAH (Gawat Darurat)</h5>
                    <h2 class="text-danger font-weight-bold" id="count-merah">0</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-warning">
                <div class="card-body text-center">
                    <h5 class="card-title">🟡 KUNING (Segera)</h5>
                    <h2 class="text-warning font-weight-bold" id="count-kuning">0</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-success">
                <div class="card-body text-center">
                    <h5 class="card-title">🟢 HIJAU (Ringan)</h5>
                    <h2 class="text-success font-weight-bold" id="count-hijau">0</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-info">
                <div class="card-body text-center">
                    <h5 class="card-title">🔵 BIRU (Umum)</h5>
                    <h2 class="text-info font-weight-bold" id="count-biru">0</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Triage Table -->
    <div class="row">
        <div class="col-md-12">
            <div class="card shadow">
                <div class="card-header bg-dark text-white">
                    <h5 class="mb-0">Data Registrasi Triase (Real-time)</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover" id="triage-table">
                            <thead class="table-dark">
                                <tr>
                                    <th>#</th>
                                    <th>Waktu Registrasi</th>
                                    <th>Nama Pasien</th>
                                    <th>Kategori</th>
                                    <th>Gejala</th>
                                    <th>RS Tujuan</th>
                                    <th>Nomor Antrean</th>
                                    <th>Status</th>
                                    <th>Aksi</th>
                                </tr>
                            </thead>
                            <tbody id="triage-tbody">
                                <tr class="text-center">
                                    <td colspan="9">Memuat data...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .card {
        transition: all 0.3s ease;
    }
    .card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transform: translateY(-3px);
    }
    
    .table tbody tr {
        transition: all 0.2s ease;
    }
    
    .table tbody tr:hover {
        background-color: #f8f9fa !important;
    }
    
    .badge-merah { background-color: #dc3545; }
    .badge-kuning { background-color: #ffc107; }
    .badge-hijau { background-color: #28a745; }
    .badge-biru { background-color: #17a2b8; }
</style>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    // Polling interval dalam milidetik
    const POLL_INTERVAL = 3000; // Update setiap 3 detik

    function loadTriageData() {
        fetch('/api/triage/registrations')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateTriageTable(data.data);
                    updateStatistics(data.data);
                }
            })
            .catch(error => console.error('Error loading triage data:', error));
    }

    function updateTriageTable(data) {
        const tbody = document.getElementById('triage-tbody');
        
        // Jika tidak ada data
        if (!data.data || data.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted">Belum ada data triase</td></tr>';
            return;
        }

        // Generate table rows
        tbody.innerHTML = data.data.map((item, index) => {
            const categoryBadge = getCategoryBadge(item.kategori);
            const statusBadge = getStatusBadge(item.status);
            
            return `
                <tr>
                    <td>${index + 1}</td>
                    <td>${formatDate(item.created_at)}</td>
                    <td><strong>${item.nama_pasien}</strong></td>
                    <td><span class="badge ${categoryBadge}">${item.kategori}</span></td>
                    <td title="${item.gejala}">${truncateText(item.gejala, 50)}</td>
                    <td>${item.rs_tujuan}</td>
                    <td><code>${item.nomor_antrean}</code></td>
                    <td><span class="badge ${statusBadge}">${item.status.toUpperCase()}</span></td>
                    <td>
                        <button class="btn btn-sm btn-info" onclick="viewDetail(${item.id})">Detail</button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    function updateStatistics(data) {
        let stats = {
            MERAH: 0,
            KUNING: 0,
            HIJAU: 0,
            BIRU: 0
        };

        data.data.forEach(item => {
            if (stats.hasOwnProperty(item.kategori)) {
                stats[item.kategori]++;
            }
        });

        document.getElementById('count-merah').textContent = stats.MERAH;
        document.getElementById('count-kuning').textContent = stats.KUNING;
        document.getElementById('count-hijau').textContent = stats.HIJAU;
        document.getElementById('count-biru').textContent = stats.BIRU;
    }

    function getCategoryBadge(kategori) {
        const categoryMap = {
            'MERAH': 'badge badge-danger badge-merah',
            'KUNING': 'badge badge-warning badge-kuning',
            'HIJAU': 'badge badge-success badge-hijau',
            'BIRU': 'badge badge-info badge-biru'
        };
        return categoryMap[kategori] || 'badge badge-secondary';
    }

    function getStatusBadge(status) {
        const statusMap = {
            'pending': 'badge-warning',
            'confirmed': 'badge-success',
            'processed': 'badge-secondary'
        };
        return statusMap[status] || 'badge-secondary';
    }

    function formatDate(dateString) {
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        return new Date(dateString).toLocaleString('id-ID', options);
    }

    function truncateText(text, length) {
        return text.length > length ? text.substring(0, length) + '...' : text;
    }

    function viewDetail(id) {
        alert('Detail view untuk ID: ' + id + ' (akan diimplementasikan)');
        // TODO: Implementasi modal detail
    }

    // Initial load
    loadTriageData();

    // Auto-refresh setiap 3 detik
    setInterval(loadTriageData, POLL_INTERVAL);
</script>
@endsection
