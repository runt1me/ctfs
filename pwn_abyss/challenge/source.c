#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#define MAX_ARG_SIZE    512
#define CRED_FILE       ".creds"

enum {
    LOGIN = 0,
    READ,
    EXIT,
};

int logged_in = 0;
static char VALID_USER[64];
static char VALID_PASS[64];

void cmd_login()
{
    char pass[MAX_ARG_SIZE] = {0};
    char user[MAX_ARG_SIZE] = {0};
    char buf[MAX_ARG_SIZE];
    int i;
    puts("Received login attempt");

    memset(buf, '\0', sizeof(buf));
    if (read(0, buf, sizeof(buf)) < 0) {
        puts("Return 1");
        return;
    }

    if (strncmp(buf, "USER ", 5)) {
        puts("Return 2");
        return;
    }

    i = 5;
    while (buf[i] != '\0')
    {
        user[i - 5] = buf[i];
        i++;
    }
    user[i - 5] = '\0';

    memset(buf, '\0', sizeof(buf));
    if (read(0, buf, sizeof(buf)) < 0) {
        puts("Return 3");
        return;
    }

    if (strncmp(buf, "PASS ", 5)) {
    	puts("Return 4");
        return;
    }

    i = 5;
    while (buf[i] != '\0')
    {
        pass[i - 5] = buf[i];
        i++;
    }
    pass[i - 5] = '\0';

    if (!strcmp(VALID_USER, user) && !strcmp(VALID_PASS, pass))
    {
        logged_in = 1;
        puts("Successful login");
    }
    else {
    	puts("Login failed");
    }
}

void cmd_read()
{
    int fd;
    int ret;
    char buf[MAX_ARG_SIZE] = {0};

    if (!logged_in)
    {
        puts("Not logged in");
        return;
    }

    puts("cmd_read: logged in");

    if (read(0, buf, sizeof(buf)) <= 0) {
        puts("cmd_read: read from buf failed?");
        return;
    }

    puts("cmd_read: read successfully from buf");

    fd = open(buf, O_RDONLY);
    if (fd < 0)
    {
        perror("open");
        return;
    }

    puts("cmd_read: open successful");

    ret = read(fd, buf, sizeof(buf));
    if (ret < 0)
    {
        perror("read");
        close(fd);
        return;
    }
    puts("cmd_read: read file successful");

    write(1, buf, ret);
    close(fd);
}

int main()
{
    int cmd;
    int fd;
    char buf[4096] = {0};
    char *tok;

    fd = open(CRED_FILE, O_RDONLY);
    if (fd < 0)
    {
        perror("open");
        puts("Does " CRED_FILE " exist?");
        return 1;
    }

    puts("Successfully opened credential file");

    if (read(fd, buf, sizeof(buf)) == 0)
    {
        puts("Credential file empty");
        close(fd);
        return 1;
    }

    close(fd);
    puts("Successfully read credential file");

    if (buf[strlen(buf) - 1] == '\n')
        buf[strlen(buf) - 1] = '\0';

    tok = strchr(buf, ':');
    if (tok == NULL)
    {
        puts("Invalid credential format");
        return 1;
    }

    if (tok - buf > sizeof(VALID_USER) - 1)
    {
        puts("Username too long");
        return 1;
    }

    if (strlen(tok + 1) > sizeof(VALID_PASS) - 1)
    {
        puts("Password too long");
        return 1;
    }
    puts("Validated username and password in credential file");

    *tok = '\0';
    strcpy(VALID_USER, buf);
    strcpy(VALID_PASS, tok + 1);

    puts("Beginning loop");
    while (1)
    {
        if (read(0, &cmd, sizeof(cmd)) != sizeof(cmd)) {
            puts("Read failed?");
            return 1;
	}

        puts("Received command");
        switch (cmd)
        {
            case LOGIN:
		puts("In case: LOGIN");
                cmd_login();
                break;
            case READ:
		puts("In case: READ");
                cmd_read();
                break;
            case EXIT:
		puts("In case: EXIT");
                return 0;
            default:
                puts("Invalid command");
                break;
        }
    }

    return 0;
}
