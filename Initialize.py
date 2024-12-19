import psutil
import requests

def get_ipv4():
    # 네트워크 인터페이스 정보 가져오기
    interfaces = psutil.net_if_addrs()
    
    for addrs in interfaces.values():
        for addr in addrs:
            # IPv4 주소만 반환
            if addr.family.name == 'AF_INET':
                return addr.address
    return "IP 주소를 찾을 수 없습니다."

def get_permission_and_settings(ip_address):
    try:
        # 원격 파일 가져오기
        url = "https://raw.githubusercontent.com/onyxofcoma/-/refs/heads/main/setting.ini"
        response = requests.get(url)
        response.raise_for_status()

        # 파일 내용 분석
        file_content = response.text
        lines = file_content.splitlines()

        user_section = False
        permission = "unauthorized"

        for line in lines:
            line = line.strip()

            # [user] 섹션 시작 확인
            if line.lower() == "[user]":
                user_section = True
                continue

            # 섹션 종료 확인
            if line.startswith("[") and line.endswith("]") and line.lower() != "[user]":
                user_section = False

            # IP에 따른 권한 확인
            if user_section and ip_address in line:
                if "admin" in line:
                    permission = "admin"
                elif "limited" in line:
                    permission = "limited"
                break

        # 권한 섹션에서 설정 값 가져오기
        if permission != "unauthorized":
            permission_section = False
            settings = {"excute_time": None, "delay_refresh": None, "delay_loading": None}

            for line in lines:
                line = line.strip()

                # 권한 섹션 시작 확인
                if line.lower() == f"[{permission}]":
                    permission_section = True
                    continue

                # 섹션 종료 확인
                if line.startswith("[") and line.endswith("]") and line.lower() != f"[{permission}]":
                    permission_section = False

                # 설정 값 가져오기
                if permission_section:
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key, value = key.strip(), value.strip()

                        if key in settings:
                            settings[key] = int(value)

            return permission, settings["excute_time"], settings["delay_refresh"], settings["delay_loading"]

    except requests.RequestException as e:
        print(f"원격 파일을 가져오는 데 실패했습니다: {e}")

    return "unauthorized", None, None, None

# 실행 로직
ip_address = get_ipv4()
permission, excute_time, delay_refresh, delay_loading = get_permission_and_settings(ip_address)

# 결과 출력 (테스트 용)
print(f"IP Address: {ip_address}")
print(f"Permission: {permission}")
print(f"Execute Time: {excute_time}")
print(f"Delay Refresh: {delay_refresh}")
print(f"Delay Loading: {delay_loading}")
