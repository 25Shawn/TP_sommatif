USE DutilShawn_TPSommatif;
#Create a user
CREATE USER IF NOT EXISTS 'shawn' IDENTIFIED BY 'shawn';
GRANT SELECT, INSERT, UPDATE, DELETE ON DutilShawn_TPSommatif.* TO 'shawn';
GRANT EXECUTE ON  DutilShawn_TPSommatif.* TO 'shawn';
