#include <stdio.h>
#include <direct.h>
#include <iostream>
#include <sstream>
#include <fstream>

using namespace std;


int main(int argc, char *argv[])
{
  ifstream perc_prog ("lancement.csv");
  string ligne;

  if (!perc_prog)
  {
	cout<<"Error\n";
	system("pause");
	return -1;
  }

  getline (perc_prog, ligne);
  while (getline (perc_prog, ligne))
  {
	//открытие файла для копирования
	  ifstream infile ("percolation.exe", ifstream::binary);
	if (!infile)
    {
	  cout<<"Error\n";
	  system("pause");
	  return -1;
    }
	//чтение файла запуска
    stringstream flux (ligne);
    string L, p;
	getline (flux, p, ';');
    getline (flux, L, ';');
	//создание пути
	string chemin = _getcwd(*argv,256);
	chemin += '\\' + p;
	_mkdir(chemin.c_str());
	chemin += '\\' + L;
	_mkdir(chemin.c_str());
	string chemin2 = chemin + "\\percolation.csv";
	//копирование исполняемого файла
	ofstream file (chemin2);
	file << "p;L;L(p);R(p);T(p)\n" << p << ";" << L << endl;
	file.close();

	infile.seekg (0, infile.end);
    int longueur = infile.tellg();
    infile.seekg (0, infile.beg);
	char *ligne_copy = new char [longueur];
	infile.read(ligne_copy, longueur);
	infile.close();

	string chemin3 = chemin + "\\percolation.exe";
	ofstream outfile (chemin3, ofstream::binary);
	outfile.write(ligne_copy, longueur);
	outfile.close();
  }
  perc_prog.close();
  return 0;
}