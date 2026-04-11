<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\TriageController;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

/**
 * Endpoint Triage (Triase Darurat)
 * Digunakan oleh Python API untuk registrasi pasien
 */
Route::prefix('triage')->group(function () {
    // POST: Menerima data triase dari Python
    Route::post('/registration', [TriageController::class, 'store']);
    
    // GET: Menampilkan semua data triase
    Route::get('/registrations', [TriageController::class, 'index']);
    
    // GET: Detail satu triase
    Route::get('/registrations/{id}', [TriageController::class, 'show']);
});

// Alias untuk kemudahan (bisa diakses dari Python)
Route::post('/triage-registration', [TriageController::class, 'store']);
