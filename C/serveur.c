#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>


int cree_socket_tcp_ip()
 {
  int sock;
  struct sockaddr_in adresse;
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
   {
    fprintf(stderr, "Erreur socket\n");
    return -1;
   }
  memset(&adresse, 0, sizeof(struct sockaddr_in));
  adresse.sin_family = AF_INET;
  // donner un numro de port disponible quelconque
  adresse.sin_port = htons(0);
  // aucun controle sur l’adresse IP :
  //adresse.sin_addr.s_addr = htons(INADDR_ANY);
  // Autre exemple :
  // connexion sur le port 33016 fix
  // adresse.sin_port = htons(33016);
  // depuis localhost seulement :
  inet_aton("192.168.1.31", &adresse.sin_addr);
  if (bind(sock, (struct sockaddr*) &adresse, sizeof(struct sockaddr_in)) < 0)
   {
    close(sock);
    fprintf(stderr, "Erreur bind\n");
    return -1;
   }
  return sock;
 }

void traite_connection(int sock)
 {
   printf("Serveur\n");
   
   char tab[100];
   char t[100];
   sprintf(tab,"Bienvenue\n");
   write(sock,tab,10*sizeof(char));
   
   read(sock,t,100*sizeof(char));
   
   printf("%s\n",t);
   
   close(sock);
 }

int affiche_adresse_socket(int sock)
 {
  struct sockaddr_in adresse;
  socklen_t longueur;
  longueur = sizeof(struct sockaddr_in);
  if (getsockname(sock, (struct sockaddr*)&adresse, &longueur) < 0)
   {
    fprintf(stderr, "Erreur getsockname\n");
    return -1;
   }
  printf("IP = %s, Port = %u\n", inet_ntoa(adresse.sin_addr), ntohs(adresse.sin_port));
  return 0;
 }

int main(void)
 {
  int sock_contact;
  int sock_connectee;
  struct sockaddr_in adresse;
  socklen_t longueur;
  pid_t pid_fils;
  sock_contact = cree_socket_tcp_ip();
  
  if (sock_contact < 0)
  return -1;
  listen(sock_contact, 5);
  printf("Mon adresse (sock contact) -> ");
  affiche_adresse_socket(sock_contact);
  
  while (1)
   {
    longueur = sizeof(struct sockaddr_in);
    sock_connectee = accept(sock_contact, (struct sockaddr*)&adresse, &longueur);
    if (sock_connectee < 0)
     {
      fprintf(stderr, "Erreur accept\n");
      return -1;
     }
    pid_fils = fork();
    if (pid_fils == -1)
     {
      fprintf(stderr, "Erreur fork\n");
      return -1;
     }
    if (pid_fils == 0) /* fils */
     {
      close(sock_contact);
      traite_connection(sock_connectee);
      exit(0);
     }
    else
   close(sock_connectee);
  }
return 0;
}
