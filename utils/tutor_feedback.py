def get_feedback(student_name, attendance_score, activity_score, task_score):
    feedbacks = []
    if attendance_score == 0:
        feedbacks.append(f"{student_name} tidak hadir di seluruh sesi pelajaran bulan ini. Kami ingin membantu agar {student_name} bisa kembali mengikuti pelajaran dengan lebih baik. Kami akan menghubungi Anda untuk membahas solusi yang tepat.")
    elif attendance_score == 1:
        feedbacks.append(f"{student_name} hadir hanya di 1 dari 4 sesi pelajaran bulan ini. Kami khawatir ini bisa mempengaruhi pemahaman materi yang diajarkan. Jika memungkinkan, mari kita diskusikan bagaimana agar {student_name} bisa lebih rutin mengikuti pelajaran.")
    elif attendance_score == 2:
        feedbacks.append(f"{student_name} hanya hadir di 2 dari 4 sesi bulan ini. Kami melihat kehadiran yang tidak konsisten mulai mempengaruhi kemajuan belajar. Akan lebih baik jika {student_name} bisa hadir lebih teratur agar tidak tertinggal materi.")
    elif attendance_score == 3:
        feedbacks.append(f"{student_name} mengikuti 3 dari 4 sesi pelajaran bulan ini. Kehadirannya cukup baik, dan meskipun ada satu sesi yang terlewat, {student_name} tetap mengikuti materi dengan baik. Kami yakin kehadiran yang lebih konsisten akan membuat belajarnya lebih maksimal!")
    elif attendance_score == 4:
        feedbacks.append(f"{student_name} selalu hadir di setiap sesi pelajaran dan menunjukkan antusiasme yang tinggi. Kami sangat menghargai kehadirannya yang konsisten, ini adalah langkah penting dalam proses belajarnya. Terus semangat, ya!")
    

    if activity_score == 0:
        feedbacks.append(f"{student_name} tampak mengalami kesulitan dalam mengikuti pelajaran terakhir. Kurangnya fokus menyebabkan {student_name} tidak sepenuhnya menangkap materi. Kami menyarankan agar {student_name} lebih terlibat aktif dalam kelas agar pemahaman terhadap pelajaran meningkat. Jika Anda memerlukan bantuan atau rekaman kelas, kami siap memberikan dukungan tambahan.")
    elif activity_score == 1:
        feedbacks.append(f"{student_name} cenderung lebih diam di kelas dan jarang terlibat dalam diskusi. Kami menyarankan agar {student_name} lebih terbuka untuk bertanya atau berinteraksi sehingga bisa lebih mudah memahami materi. Jika ada kendala tertentu, kami siap membantu agar suasana kelas lebih nyaman untuk belajar.")
    elif activity_score == 2:
        feedbacks.append(f"{student_name} cukup fokus di kelas meskipun jarang bertanya. Namun, {student_name} selalu memperhatikan dengan baik dan mengikuti instruksi dengan seksama. Mungkin dengan lebih banyak berpartisipasi dalam diskusi, {student_name} bisa meningkatkan pemahaman materi. Secara keseluruhan, {student_name} sudah menunjukkan perkembangan yang positif.")
    elif activity_score == 3:
        feedbacks.append(f"{student_name} sangat terlibat dalam setiap sesi, aktif berpartisipasi dalam diskusi, dan tidak ragu mengajukan pertanyaan yang mendalam. {student_name} selalu menunjukkan kemajuan yang baik dan memahami materi dengan cepat. Saya sering memberikan tantangan tambahan untuk membantu {student_name} terus berkembang dan belajar lebih jauh.")

    if task_score == 0:
        feedbacks.append(f"{student_name} tampaknya menghadapi beberapa tantangan dalam menyelesaikan tugas kali ini. Sangat penting bagi {student_name} untuk meluangkan lebih banyak waktu dalam berlatih agar pemahamannya terhadap materi semakin kuat. Kami berharap {student_name} bisa mengejar ketinggalan. Jika ada kesulitan, jangan ragu untuk menghubungi saya, saya siap membantu.")
    elif task_score == 1:
        feedbacks.append(f"{student_name} berhasil menyelesaikan sebagian besar tugas dengan baik, namun ada beberapa area yang memerlukan sedikit perbaikan. Dengan latihan tambahan dan perhatian lebih, {student_name} pasti akan bisa meningkatkan kualitas tugas-tugasnya dan mencapai hasil yang lebih baik lagi.")
    elif task_score == 2:
        feedbacks.append(f"{student_name} telah berhasil menyelesaikan semua tugas dengan sangat baik. Pemahamannya terhadap materi sangat jelas, dan {student_name} mampu menyelesaikan setiap tugas tepat waktu. Senang sekali melihat kemajuannya yang terus meningkat. Terus lanjutkan usaha ini, ya!")

    return feedbacks



def get_tutor_feedback(student_name):
    return f"""Halo, Ayah/Bunda dari {student_name}! 👋

Saya Azhar Faturohman Ahidin, tutor {student_name} di Sekolah Pemrograman Internasional Algonova.

Saya ingin berbagi kabar tentang perkembangan {student_name} selama satu bulan terakhir. Kami telah menilai kemajuan {student_name} berdasarkan keterampilan yang dipelajari di kelas, serta upaya yang telah ditunjukkan dalam menyelesaikan berbagai tugas. 😊 Hasil lengkapnya bisa Anda lihat pada lampiran yang sudah kami sediakan 📄.

Jika ada hal yang ingin ditanyakan mengenai hasil ini atau tentang perkembangan {student_name}, saya siap membantu menjelaskan lebih lanjut. Terima kasih atas dukungan Anda dalam proses belajar {student_name}, dan mari kita terus bekerja sama untuk mencapai hasil yang lebih baik ke depannya!"""