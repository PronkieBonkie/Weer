//algemeen updaten
stap 1
sudo apt update
sudo apt upgrade

// mysql downloaden
stap 2
sudo apt install mariadb-server

// mysql instellen
stap 3
sudo mysql_secure_installation

//aantal vragen voor instellen mysql
stap 4 
prompt beantwoorden 

//-u = declareren van user -p is het vragen na enter voor password die in stap 4 is aangemaakt.
stap 5 
sudo mysql -u root -p

// configuratie om ip adressen in te stellen veranderen naar bind-address = 0.0.0.0
stap 6
sudo nano /etc/mysql/my.cnf
