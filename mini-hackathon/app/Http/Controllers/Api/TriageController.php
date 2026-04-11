<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\TriageRegistration;
use Illuminate\Http\Request;

class TriageController extends Controller
{
    /**
     * Menerima data triase dari Python API dan menyimpan ke database
     * Endpoint: POST /api/triage-registration
     */
    public function store(Request $request)
    {
        try {
            // Validasi input dari Python
            $validated = $request->validate([
                'nama' => 'required|string|max:255',
                'kategori' => 'required|in:MERAH,KUNING,HIJAU,BIRU',
                'gejala' => 'required|string',
                'rs_tujuan' => 'required|string|max:255',
                'lokasi_user' => 'nullable|string',
                'jarak_km' => 'nullable|numeric'
            ]);

            // Generate nomor antrean unik
            $timestamp = now()->format('YmdHis');
            $random = str_pad(rand(0, 999), 3, '0', STR_PAD_LEFT);
            $nomor_antrean = "TRIAGE-{$timestamp}-{$random}";

            // Simpan ke database
            $registration = TriageRegistration::create([
                'nama_pasien' => $validated['nama'],
                'kategori' => $validated['kategori'],
                'gejala' => $validated['gejala'],
                'rs_tujuan' => $validated['rs_tujuan'],
                'nomor_antrean' => $nomor_antrean,
                'lokasi_user' => $validated['lokasi_user'] ?? null,
                'jarak_km' => $validated['jarak_km'] ?? null,
                'status' => 'pending'
            ]);

            // Tentukan prioritas berdasarkan kategori
            $prioritas = in_array($validated['kategori'], ['MERAH', 'KUNING']) ? 'PRIORITAS' : 'NORMAL';

            return response()->json([
                'status' => 'success',
                'pesan' => 'Data triase berhasil disimpan',
                'nomor_antrean' => $nomor_antrean,
                'prioritas' => $prioritas,
                'kategori' => $validated['kategori'],
                'rs_tujuan' => $validated['rs_tujuan'],
                'data' => $registration
            ], 201);

        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json([
                'status' => 'error',
                'pesan' => 'Validasi gagal',
                'errors' => $e->errors()
            ], 422);

        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'pesan' => 'Terjadi kesalahan: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Menampilkan semua data triase (untuk dashboard)
     */
    public function index()
    {
        $registrations = TriageRegistration::latest()->paginate(50);
        
        return response()->json([
            'status' => 'success',
            'data' => $registrations
        ]);
    }

    /**
     * Menampilkan detail satu triase
     */
    public function show($id)
    {
        $registration = TriageRegistration::find($id);

        if (!$registration) {
            return response()->json([
                'status' => 'error',
                'pesan' => 'Data tidak ditemukan'
            ], 404);
        }

        return response()->json([
            'status' => 'success',
            'data' => $registration
        ]);
    }
}
