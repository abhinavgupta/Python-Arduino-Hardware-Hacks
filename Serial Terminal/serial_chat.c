/*

 * Arduino-serial

 * --------------

 * 

 * A simple command-line example program showing how a computer can

 * communicate with an Arduino board. Works on any POSIX system (Mac/Unix/PC) 

 *

 *

 *

 * 

 *

 * 

 * 

 *

 */



#include <stdio.h>    /* Standard input/output definitions */

#include <stdlib.h> 

#include <stdint.h>   /* Standard types */

#include <string.h>   /* String function definitions */

#include <unistd.h>   /* UNIX standard function definitions */

#include <fcntl.h>    /* File control definitions */

#include <errno.h>    /* Error number definitions */

#include <termios.h>  /* POSIX terminal control definitions */

#include <sys/ioctl.h>

#include <getopt.h>



void usage(void);

int serialport_init(const char* serialport, int baud);

int serialport_writebyte(int fd, uint8_t b);

int serialport_write(int fd, const char* str);

int serialport_read_until(int fd, char* buf, char until);



void usage(void) {

    printf("Usage: arduino-serial -p <serialport> [OPTIONS]\n"

    "\n"

    "Options:\n"

    "  -h, --help                   Print this help message\n"

    "  -p, --port=serialport        Serial port Arduino is on\n"

    "  -b, --baud=baudrate          Baudrate (bps) of Arduino\n"

    "  -s, --send=data              Send data to Arduino\n"

    "  -r, --receive                Receive data from Arduino & print it out\n"

    "  -n  --num=num                Send a number as a single byte\n"

    "  -d  --delay=millis           Delay for specified milliseconds\n"

    "\n"

    "Note: Order is important. Set '-b' before doing '-p'. \n"

    "      Used to make series of actions:  '-d 2000 -s hello -d 100 -r' \n"

    "      means 'wait 2secs, send 'hello', wait 100msec, get reply'\n"

    "\n");

}



int main(int argc, char *argv[]) 

{

    int fd = 0;

    char serialport[256];

    int baudrate = B115200;  // default

    char buf[20], dat[2], use[1];

    int rc,n;



      //baudrate = 9600;

      fd = serialport_init("/dev/ttyUSB0", baudrate);

                  if(fd==-1) return -1;

      usleep(3000 * 1000 );

            

      while(1) {

            strcpy(dat, "00\0");

            fgets(use,8,stdin);

            if(use[0] == 'i') {

                  dat[0] = '1';

                  dat[1] = 58;

            }

            else if(use[0] == 'k') {

                  dat[0] = '2';

                  dat[1] = 58;

            }

            else if(use[0] == 'j') {

                  dat[0] = '3';

                  dat[1] = 58;

            }

            else if(use[0] == 'l') {

                  dat[0] = '4';

                  dat[1] = 58;

            }

                  
            printf("%s\n",dat);
            rc = serialport_write(fd, dat);

                        if(rc==-1) return -1;

             //printf("Waiting until UART buffer clears: %d\n", tcdrain(fd));

             n = serialport_read_until(fd, buf, ':');

               printf("wrote %d bytes, read %d bytes: %s\n", rc, n, buf);

      }



       close(fd);



    exit(EXIT_SUCCESS);    

} // end main

    

int serialport_writebyte( int fd, uint8_t b)

{

    int n = write(fd,&b,1);

    if( n!=1)

        return -1;

    return 0;

}



int serialport_write(int fd, const char* str)

{

    int len = strlen(str);

    int n = write(fd, str, len);

    if( n!=len ) 

        return -1;

    return n;

}



int serialport_read_until(int fd, char* buf, char until)

{

    char b[1];

    int i=0;

    do { 

        int n = read(fd, b, 1);  // read a char at a time

        if( n==-1) return -1;    // couldn't read

        if( n==0 ) {

            usleep( 10 * 1000 ); // wait 10 msec try again

            continue;

        }

        buf[i] = b[0]; i++;

    } while( b[0] != until );



    buf[i] = 0;  // null terminate the string

    return i;

}



// takes the string name of the serial port (e.g. "/dev/tty.usbserial","COM1")

// and a baud rate (bps) and connects to that port at that speed and 8N1.

// opens the port in fully raw mode so you can send binary data.

// returns valid fd, or -1 on error

int serialport_init(const char* serialport, int baud)

{

    struct termios toptions;

    int fd;

    

    //fprintf(stderr,"init_serialport: opening port %s @ %d bps\n",

    //        serialport,baud);



    //fd = open(serialport, O_RDWR | O_NOCTTY | O_NDELAY);

    fd = open(serialport, O_RDWR | O_NOCTTY);

    if (fd == -1)  {

        perror("init_serialport: Unable to open port ");

        return -1;

    }

    

    if (tcgetattr(fd, &toptions) < 0) {

        perror("init_serialport: Couldn't get term attributes");

        return -1;

    }

    speed_t brate = baud; // let you override switch below if needed

    switch(baud) {

    case 4800:   brate=B4800;   break;

    case 9600:   brate=B9600;   break;

// if you want these speeds, uncomment these and set #defines if Linux

//#ifndef OSNAME_LINUX

//    case 14400:  brate=B14400;  break;

//#endif

    case 19200:  brate=B19200;  break;

//#ifndef OSNAME_LINUX

//    case 28800:  brate=B28800;  break;

//#endif

    //case 28800:  brate=B28800;  break;

    case 38400:  brate=B38400;  break;

    case 57600:  brate=B57600;  break;

    case 115200: brate=B115200; break;

    }

    cfsetispeed(&toptions, brate);

    cfsetospeed(&toptions, brate);



    // 8N1

    toptions.c_cflag &= ~PARENB;

    toptions.c_cflag &= ~CSTOPB;

    toptions.c_cflag &= ~CSIZE;

    toptions.c_cflag |= CS8;

    // no flow control

    toptions.c_cflag &= ~CRTSCTS;



    toptions.c_cflag |= CREAD | CLOCAL;  // turn on READ & ignore ctrl lines

    toptions.c_iflag &= ~(IXON | IXOFF | IXANY); // turn off s/w flow ctrl



    toptions.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); // make raw

    toptions.c_oflag &= ~OPOST; // make raw



    // see: http://unixwiz.net/techtips/termios-vmin-vtime.html

    toptions.c_cc[VMIN]  = 0;

    toptions.c_cc[VTIME] = 20;

    

    if( tcsetattr(fd, TCSANOW, &toptions) < 0) {

        perror("init_serialport: Couldn't set term attributes");

        return -1;

    }



    return fd;

}

