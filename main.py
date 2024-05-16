import collections

# Константы
LOG_FILE_PATH = 'access.log'
TARGET_STATUS_CODE = 500
TOP_N = 10

def parse_log_file(file_path):
    def is_valid_line(line):
        return not line.startswith('#') and len(line.strip().split(';')) == 5

    def extract_src_ip_if_target_status(line):
        parts = line.strip().split(';')
        src_ip, dest_ip, http_code, http_path, resp_bytes = parts
        return src_ip if int(http_code) == TARGET_STATUS_CODE else None

    src_ips = []
    with open(file_path, 'r') as file:
        for line in file:
            if is_valid_line(line):
                src_ip = extract_src_ip_if_target_status(line)
                if src_ip:
                    src_ips.append(src_ip)
    return src_ips

def get_top_n_src_ips(src_ips, n):
    counter = collections.Counter(src_ips)
    most_common = counter.most_common(n)
    return [ip for ip, count in most_common][::-1]

def main():
    src_ips = parse_log_file(LOG_FILE_PATH)
    top_src_ips = get_top_n_src_ips(src_ips, TOP_N)
    for i, ip in enumerate(top_src_ips, start=1):
        print(f"{TOP_N + 1 - i}: {ip}")

if __name__ == "__main__":
    main()