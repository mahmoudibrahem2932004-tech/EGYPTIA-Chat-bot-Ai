# استخدام نسخة راسا المناسبة لمشروعك
FROM rasa/rasa:3.6.2

# تحديد مسار العمل داخل الحاوية
WORKDIR /app

# نسخ كل ملفات المشروع (بما فيها start.sh و requirements.txt)
COPY . /app

# التبديل لمستخدم root لضمان الصلاحيات
USER root

# إعطاء صلاحية التنفيذ لملف الـ start.sh
RUN chmod +x start.sh

# تثبيت المكتبات من ملف requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# فتح البورت المطلوب (مناسب لـ Hugging Face)
EXPOSE 7860

# مسح أي Entrypoint قديم لضمان تشغيل السكريبت بتاعنا فقط
ENTRYPOINT []

# تشغيل السكريبت اللي بيقوم الـ Rasa والـ Action Server مع بعض
CMD ["/bin/bash", "./start.sh"]