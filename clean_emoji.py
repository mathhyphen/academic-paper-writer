# Clean emoji from Python file
with open(r'D:\apps\academic-paper-writer\academic_paper_writer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all emoji characters (Unicode ranges for emoji)
import re

# Remove common emoji
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)

content = emoji_pattern.sub('', content)

# Also remove checkmarks and other symbols
content = content.replace('✅', '[OK]').replace('✔', '[OK]').replace('❌', '[FAIL]')
content = content.replace('⚠️', '[WARN]').replace('📊', '[DATA]').replace('📝', '[WRITE]')
content = content.replace('📥', '[DOWNLOAD]').replace('🔍', '[SEARCH]').replace('🎯', '[TARGET]')
content = content.replace('📋', '[LIST]').replace('💡', '[IDEA]').replace('🚀', '[LAUNCH]')
content = content.replace('📄', '[FILE]').replace('📁', '[FOLDER]').replace('🏆', '[AWARD]')
content = content.replace('✨', '[STAR]').replace('💰', '[MONEY]').replace('🌐', '[WEB]')
content = content.replace('📈', '[CHART]').replace('🎉', '[CELEBRATE]').replace('🔧', '[TOOLS]')
content = content.replace('📚', '[BOOKS]').replace('🔬', '[RESEARCH]').replace('💻', '[CODE]')
content = content.replace('📅', '[CALENDAR]').replace('🔬', '[SCIENCE]').replace('💡', '[TIP]')

with open(r'D:\apps\academic-paper-writer\academic_paper_writer.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Emoji removed successfully!")
