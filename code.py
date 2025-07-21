from librouteros import connect

def main():
    # Read router IPs from file
    with open('ips.txt') as f:
        ips = [line.strip() for line in f if line.strip()]

    username = 'admin'
    password = 'admin'
    usercondition=False
    for ip in ips:
        print(f"Connecting to router {ip}...")
        try:
            api = connect(host=ip, username=username, password=password)

            # Get list of users on the router
            users = api(cmd='/user/print')

            # Check if user 'group' already exists
            user_exists = False
            for user in users:
                if user.get('name') == 'group':
                    user_exists = True
                    break
            #check if user exists
            if user_exists:
                print(f"User 'group' already exists on {ip}")
            else:
                # Add new user and print response
                usercondition=True
                response = api(cmd='/user/add', name='group', password='group', group='full')
                print(f"Add user response on {ip}: {list(response)}")
            if(usercondition):
                print("User Created")
            # Disable unwanted services and change Winbox port
            services = api(cmd='/ip/service/print')
            for service in services:
                service_id = service.get('.id')
                name = service.get('name')

                if name in ['telnet', 'ftp', 'www']:
                    api(cmd='/ip/service/set', numbers=service_id, disabled='yes')
                    print(f"Disabled {name} service on {ip}")
                elif name == 'winbox':
                    api(cmd='/ip/service/set', numbers=service_id, port='50000')
                    print(f"Changed Winbox port on {ip} to 50000")

            api.close()
            print(f"Finished configuration on {ip}\n")

        except Exception as e:
            print(f"Failed to connect or configure {ip}: {e}")

if __name__ == "__main__":
    main()
