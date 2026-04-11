<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class TriageRegistration extends Model
{
    protected $table = 'triage_registrations';

    protected $fillable = [
        'nama_pasien',
        'kategori',
        'gejala',
        'rs_tujuan',
        'nomor_antrean',
        'lokasi_user',
        'jarak_km',
        'status'
    ];

    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];
}
