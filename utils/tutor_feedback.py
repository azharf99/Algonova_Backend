def get_feedback(student_name, attendance_number):
    if attendance_number == 0:
        return f"{student_name} tidak hadir di seluruh sesi pelajaran bulan ini. Kami ingin membantu agar {student_name} bisa kembali mengikuti pelajaran dengan lebih baik. Kami akan menghubungi Anda untuk membahas solusi yang tepat."
    elif attendance_number == 1:
        return f"{student_name} hadir hanya di 1 dari 4 sesi pelajaran bulan ini. Kami khawatir ini bisa mempengaruhi pemahaman materi yang diajarkan. Jika memungkinkan, mari kita diskusikan bagaimana agar {student_name} bisa lebih rutin mengikuti pelajaran."
    elif attendance_number == 2:
        return f"{student_name} hanya hadir di 2 dari 4 sesi bulan ini. Kami melihat kehadiran yang tidak konsisten mulai mempengaruhi kemajuan belajar. Akan lebih baik jika {student_name} bisa hadir lebih teratur agar tidak tertinggal materi."
    elif attendance_number == 3:
        return f"{student_name} mengikuti 3 dari 4 sesi pelajaran bulan ini. Kehadirannya cukup baik, dan meskipun ada satu sesi yang terlewat, {student_name} tetap mengikuti materi dengan baik. Kami yakin kehadiran yang lebih konsisten akan membuat belajarnya lebih maksimal!"
    elif attendance_number == 4:
        return f"{student_name} selalu hadir di setiap sesi pelajaran dan menunjukkan antusiasme yang tinggi. Kami sangat menghargai kehadirannya yang konsisten, ini adalah langkah penting dalam proses belajarnya. Terus semangat, ya!."
    


def get_tutor_feedback(student_name):
    return f"""Halo, Ayah/Bunda dari {student_name}! 👋

Saya Azhar Faturohman Ahidin, tutor {student_name} di Sekolah Pemrograman Internasional Algonova.

Saya ingin berbagi kabar tentang perkembangan {student_name} selama satu bulan terakhir. Kami telah menilai kemajuan {student_name} berdasarkan keterampilan yang dipelajari di kelas, serta upaya yang telah ditunjukkan dalam menyelesaikan berbagai tugas. 😊 Hasil lengkapnya bisa Anda lihat pada lampiran yang sudah kami sediakan 📄.

Jika ada hal yang ingin ditanyakan mengenai hasil ini atau tentang perkembangan {student_name}, saya siap membantu menjelaskan lebih lanjut. Terima kasih atas dukungan Anda dalam proses belajar {student_name}, dan mari kita terus bekerja sama untuk mencapai hasil yang lebih baik ke depannya!"""