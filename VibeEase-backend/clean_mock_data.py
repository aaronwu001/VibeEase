import os
import json

INPUT_DIR = './Knot_Data'
OUTPUT_DIR = './cleaned_Knot_Data'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def detect_and_fix_json_strings(record):
    fixed_record = {}
    for key, value in record.items():
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                fixed_record[key] = parsed
            except (json.JSONDecodeError, TypeError):
                fixed_record[key] = value
        else:
            fixed_record[key] = value
    return fixed_record

for filename in os.listdir(INPUT_DIR):
    if filename.endswith('.txt'):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename.replace('.txt', '.json'))

        print(f'🔄 Now solving file: {filename}')
        fixed_data = []

        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    fixed_data = [detect_and_fix_json_strings(rec) for rec in data]
                elif isinstance(data, dict):
                    fixed_data = detect_and_fix_json_strings(data)
                else:
                    raise ValueError("Unknown data type")
            except json.JSONDecodeError:
                f.seek(0)
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        fixed_data.append(detect_and_fix_json_strings(record))
                    except Exception as e:
                        print(f'❌ jump to next line because of error: {e}')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
        print(f'✅ output: {output_path}')
