<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('triage_registrations', function (Blueprint $table) {
            $table->id();
            $table->string('nama_pasien');
            $table->enum('kategori', ['MERAH', 'KUNING', 'HIJAU', 'BIRU']); // Kategori triase
            $table->text('gejala'); // Ringkasan gejala
            $table->string('rs_tujuan'); // Nama fasilitas kesehatan tujuan
            $table->string('nomor_antrean')->unique(); // Nomor antrean dari sistem
            $table->string('lokasi_user')->nullable(); // Koordinat user
            $table->integer('jarak_km')->nullable(); // Jarak ke RS tujuan
            $table->enum('status', ['pending', 'confirmed', 'processed'])->default('pending');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('triage_registrations');
    }
};
