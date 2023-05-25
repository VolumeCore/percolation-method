#include <stdio.h>
#include <windows.h>
#include <math.h>
#include <time.h>
#include <direct.h>
#include <psapi.h>
#include "percolation.h"
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <iomanip>

using namespace std;

#define pi 3.14159265;

int p;//концентрация

using namespace std;

string nom_des_images ()
{
  time_t seconds;
  time(&seconds);

  stringstream ss;
  ss << seconds;
  string ts = ss.str();
  return ts;
}

void image (std::vector<std::vector<ter_rgb>> &term, int L, string nom)
{
  unsigned char file[14] = {
    'B','M', // magic
    0,0,0,0, // size in bytes
    0,0, // app data
    0,0, // app data
    40+14,0,0,0 // start of data offset
  };
  unsigned char info[40] = {
    40,0,0,0, // info hd size
    0,0,0,0, // width
    0,0,0,0, // heigth
    1,0, // number color planes
    24,0, // bits per pixel
    0,0,0,0, // compression is none
    0,0,0,0, // image bits size
    0x13,0x0B,0,0, // horz resoluition in pixel / m
    0x13,0x0B,0,0, // vert resolutions (0x03C3 = 96 dpi, 0x0B13 = 72 dpi)
    0,0,0,0, // #colors in pallete
    0,0,0,0, // #important colors
  };

  int w=L;
  int h=L;

  int padSize  = (4-(w*3)%4)%4;
  int sizeData = w*h*3 + h*padSize;
  int sizeAll  = sizeData + sizeof(file) + sizeof(info);

  file[2] = (unsigned char)( sizeAll    );
  file[3] = (unsigned char)( sizeAll>> 8);
  file[4] = (unsigned char)( sizeAll>>16);
  file[5] = (unsigned char)( sizeAll>>24);

  info[4] = (unsigned char)( w   );
  info[5] = (unsigned char)( w>> 8);
  info[6] = (unsigned char)( w>>16);
  info[7] = (unsigned char)( w>>24);

  info[8] = (unsigned char)( h    );
  info[9] = (unsigned char)( h>> 8);
  info[10] = (unsigned char)( h>>16);
  info[11] = (unsigned char)( h>>24);

  info[20] = (unsigned char)( sizeData    );
  info[21] = (unsigned char)( sizeData>> 8);
  info[22] = (unsigned char)( sizeData>>16);
  info[23] = (unsigned char)( sizeData>>24);

  ofstream stream (nom, ofstream::binary); 

  stream.write( (char*)file, sizeof(file) );
  stream.write( (char*)info, sizeof(info) );

  unsigned char pad[3] = {0,0,0};

  for ( int y=0; y<h; y++ )
  {
    for ( int x=0; x<w; x++ )
    {
	  unsigned char pixel[3];
	  pixel[0] = term[y][x].b;
      pixel[1] = term[y][x].g;
      pixel[2] = term[y][x].r;

      stream.write( (char*)pixel, 3 );
    }
    stream.write( (char*)pad, padSize );
  }
  stream.close();
  return;
}

float coefficient (int x1, int x2, int r_zone)
{
  float e1, e2, sigma, t;
  sigma=float(r_zone)/3.2;
  e1=e2=0;
  t=2*pi;
  e1=exp((-1)*x1*x1/(2*sigma*sigma))/(sigma*sqrt(t));
  e2=exp((-1)*x2*x2/(2*sigma*sigma))/(sigma*sqrt(t));
  return e1*e2;
}

ter_way_min carte_thermique (std::vector<std::vector<int>> term, std::vector<std::vector<float>> &term_termique, int n)
{
  //инициализация радиуса зоны влияния
  int r_zone=10;
  if (p==1) r_zone=6;
  if (p==2) r_zone=5;
  if (p>=3 && p<=4) r_zone=4;
  if (p>=5 && p<=9) r_zone=3;
  if (p>=10 && p<=43) r_zone=2;
  if (p>=44 && p<=56) r_zone=3;
  if (p>=57 && p<=63) r_zone=4;
  if (p>=64 && p<=68) r_zone=5;
  if (p>=69 && p<=71) r_zone=6;
  if (p>=72 && p<=74) r_zone=7;
  if (p>=75 && p<=76) r_zone=8;
  if (p>=77 && p<=78) r_zone=9;
  if (p>=79) r_zone=10;

  //инициализация расширенной матрицы
  vector<vector<float>> term3 (n+2*r_zone, vector<float>(n+2*r_zone));
  int i,j;
  ter_way_min max;
  max.dmin=-1;
  for (i=0;i<n;i++)
	for (j=0;j<n;j++)
	  term3[i+r_zone][j+r_zone]=term[i][j];

  //создание тепловой карты
  for (i=r_zone;i<n+r_zone;i++)
	for (j=r_zone;j<n+r_zone;j++)
	{
	  switch (r_zone)
	  {
	  case 2:
		term_termique[i-r_zone][j-r_zone]=
			term3[i-1][j-1]*coefficient(-1,-1,r_zone)
			+term3[i-1][j]*coefficient(-1,0,r_zone)
			+term3[i-1][j+1]*coefficient(-1,1,r_zone)
			+term3[i][j-1]*coefficient(0,-1,r_zone)
			+term3[i][j]*coefficient(0,0,r_zone)
			+term3[i][j+1]*coefficient(0,1,r_zone)
			+term3[i+1][j-1]*coefficient(1,-1,r_zone)
			+term3[i+1][j]*coefficient(1,0,r_zone)
			+term3[i+1][j+1]*coefficient(1,1,r_zone)
			+term3[i-2][j]*coefficient(-2,0,r_zone)
			+term3[i+2][j]*coefficient(2,0,r_zone)
			+term3[i][j-2]*coefficient(0,-2,r_zone)
			+term3[i][j+2]*coefficient(0,2,r_zone);
		break;
	  case 3:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 4:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 5:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 6:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 7:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 8:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 9:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  case 10:
		term_termique[i-r_zone][j-r_zone]=term3[i][j];
		break;
	  }
	  if (max.dmin<term_termique[i-r_zone][j-r_zone])
	  {
	    max.dmin=term_termique[i-r_zone][j-r_zone];
		max.i=i-r_zone;
		max.j=j-r_zone;
	  }
	}

  //
  switch (r_zone)
	  {
	  case 2:
		max.dmin=
			coefficient(-1,-1,r_zone)
			+coefficient(-1,0,r_zone)
			+coefficient(-1,1,r_zone)
			+coefficient(0,-1,r_zone)
			+coefficient(0,0,r_zone)
			+coefficient(0,1,r_zone)
			+coefficient(1,-1,r_zone)
			+coefficient(1,0,r_zone)
			+coefficient(1,1,r_zone)
			+coefficient(-2,0,r_zone)
			+coefficient(2,0,r_zone)
			+coefficient(0,-2,r_zone)
			+coefficient(0,2,r_zone);
		break;
	  case 3:
		max.dmin=term3[i][j];
		break;
	  case 4:
		max.dmin=term3[i][j];
		break;
	  case 5:
		max.dmin=term3[i][j];
		break;
	  case 6:
		max.dmin=term3[i][j];
		break;
	  case 7:
		max.dmin=term3[i][j];
		break;
	  case 8:
		max.dmin=term3[i][j];
		break;
	  case 9:
		max.dmin=term3[i][j];
		break;
	  case 10:
		max.dmin=term3[i][j];
		break;
	}
  return max;
}

ter_way_min way_min (std::vector<std::vector<int>> term, std::vector<std::vector<int>> &term2, int n, int beginx, int beginy, int color)
{
  ter_way_min d_min, min;
  std::vector<ter_way_min> way (0);
  int i,j;

  if (term2[beginx][beginy]==color)
  {
	i=beginx;
	for (j=0;j<n;j++)
      if (term2[i][j]==1)
	  {
		d_min.i=i;
		d_min.j=j;
		d_min.dmin=abs(j-beginy);
		way.push_back(d_min);
	  }
  }

  min.dmin=n*n+1;
  if (way.size()==0) return min;
  min=way[0];
  for (i=0;i<way.size();i++)
  {
	if (way[i].dmin<min.dmin) min=way[i];
  }

  way.clear();
  return min;
}

ter_vitesse deykstra (std::vector<std::vector<int>> term, std::vector<std::vector<int>> &term2, int n, int beginx, int beginy, int color)
{
  long long int i,j,min,xx;
  ter_vitesse stoppoint;
  std::vector<std::vector<long long int>> terd (n, std::vector<long long int>(n));
  std::vector<ter_vitesse> coor (1);

  //матрица весов пути
  for(i=0;i<n;i++)
    for (j=0;j<n;j++)
	{
	  terd[i][j]=-1;
	}
  //
  i=beginx;
  j=beginy;
  xx=0;
  if (term[i][j]==0) term2[i][j]=color;
  else term2[i][j]=color+1;
  if (term[i][j]==0) term[i][j]=color;
  else term[i][j]=color+1;

  while (i!=n-1)
  {
	min=n*n+2;
	//движение вниз
	if (i+1!=n && term[i+1][j]!=-1)
	{
	  if (term[i+1][j]==1 && (terd[i+1][j]==-1 || terd[i+1][j]>(terd[i][j]+1)))
	  {
		terd[i+1][j]=terd[i][j]+1;
	  	coor[xx].i=i+1;
	    coor[xx].j=j;
	    coor[xx].d=terd[i+1][j];
	    xx++;
	    coor.resize(xx+1);
	  }
	  if (term[i+1][j]==0 && (terd[i+1][j]==-1 || terd[i+1][j]>(terd[i][j]+n))) 
	  {
		terd[i+1][j]=terd[i][j]+n;
		coor[xx].i=i+1;
	    coor[xx].j=j;
	    coor[xx].d=terd[i+1][j];
	    xx++;
	    coor.resize(xx+1);
	  }
	}
	//движение вправо
	if (j+1!=n && term[i][j+1]!=-1)
	{
	  if (term[i][j+1]==1 && (terd[i][j+1]==-1 || terd[i][j+1]>(terd[i][j]+1)))
	  {
		terd[i][j+1]=terd[i][j]+1;
		coor[xx].i=i;
	    coor[xx].j=j+1;
	    coor[xx].d=terd[i][j+1];
	    xx++;
	    coor.resize(xx+1);
	  }
	  if (term[i][j+1]==0 && (terd[i][j+1]==-1 || terd[i][j+1]>(terd[i][j]+n))) 
	  {
		terd[i][j+1]=terd[i][j]+n;
		coor[xx].i=i;
	    coor[xx].j=j+1;
	    coor[xx].d=terd[i][j+1];
	    xx++;
	    coor.resize(xx+1);
	  }
	}
	//движение влево
	if (j-1!=-1 && term[i][j-1]!=-1)
	{
	  if (term[i][j-1]==1 && (terd[i][j-1]==-1 || terd[i][j-1]>(terd[i][j]+1)))
	  {
		terd[i][j-1]=terd[i][j]+1;
		coor[xx].i=i;
	    coor[xx].j=j-1;
	    coor[xx].d=terd[i][j-1];
	    xx++;
	    coor.resize(xx+1);
	  }
	  if (term[i][j-1]==0 && (terd[i][j-1]==-1 || terd[i][j-1]>(terd[i][j]+n)))
	  {
		terd[i][j-1]=terd[i][j]+n;
		coor[xx].i=i;
	    coor[xx].j=j-1;
	    coor[xx].d=terd[i][j-1];
	    xx++;
	    coor.resize(xx+1);
	  }
	}
	//
	long long int vitbuf=0;
	for (int yy=0;yy<coor.size()-1;yy++)
	  if (coor[yy].d<min)
	  {
	    min=coor[yy].d;
		i=coor[yy].i;
		j=coor[yy].j;
		vitbuf=yy;
	  }
	vector<ter_vitesse>::iterator pos=coor.begin()+vitbuf;
	coor.erase(pos);
	xx--;
  }
  //здесь есть все пути, но нужно отметить оптимальный путь
  stoppoint.d=min;
  if (term[i][j]==0) term2[i][j]=color;
  else term2[i][j]=color+1;

  while (true)
  {
start:
	  if (i==beginx && j==beginy) break;
	  if (i-1!=-1 && ((min-terd[i-1][j])==1 || (min-terd[i-1][j])==n))
	  {
	    i=i-1;
	    j=j;		
		min=terd[i][j];
		if (color==6 && i<beginx) goto start;
	    if (term[i][j]==0 || term[i][j]==color) term2[i][j]=color;
		else term2[i][j]=color+1;
	    goto start;
	  }
	  if (j+1!=n && ((min-terd[i][j+1])==1 || (min-terd[i][j+1])==n))
	  {
	    i=i;
	    j=j+1;
		min=terd[i][j];
		if (color==6 && i<beginx) goto start;
	    if (term[i][j]==0 || term[i][j]==color) term2[i][j]=color;
		else term2[i][j]=color+1;
	    goto start;
	  }
	if (j-1!=-1 && ((min-terd[i][j-1])==1 || (min-terd[i][j-1])==n))
	{
	  i=i;
	  j=j-1;
	  min=terd[i][j];
	  if (color==6 && i<beginx) goto start;
	  if (term[i][j]==0 || term[i][j]==color) term2[i][j]=color;
	  else term2[i][j]=color+1;
	  goto start;
    }
	if (term[i][j]==-1 || min==-1) break;
  }
  
  stoppoint.i=i;
  stoppoint.j=j;
  return stoppoint;
}

ter_vitesse way_opt (std::vector<std::vector<int>> &term, std::vector<std::vector<int>> &term2, std::vector<ter_vitesse> &way, int n, ter_vitesse point, int color)
{
  long long int i,j,t,min;
  std::vector<std::vector<int>> term3 (n, std::vector<int>(n));
  ter_vitesse holepoint, stoppoint;
  //отрисовка самого оптимального пути
  deykstra (term, term2, n, point.i, point.j, color);
  //построение оптимального маршрута
  term3=term2;
  way[0]=point;
  i=point.i;
  j=point.j;
  if (term[i][j]==0) term3[i][j]=color+2;
  else term3[i][j]=color+3;
  while (true)
  {
start:
	if (i==n-1) break;
	if (i+1!=n && (term3[i+1][j]==color || term3[i+1][j]==color+1))
	{
	  stoppoint.i=i+1;
	  stoppoint.j=j;
	  way.push_back (stoppoint);
	  if (term[i+1][j]==0 || term[i+1][j]==color) term3[i+1][j]=color+2;
	  else term3[i+1][j]=color+3;
	  i=i+1;
	  j=j;
	  goto start;
	}
	if (j+1!=n && (term3[i][j+1]==color || term3[i][j+1]==color+1))
	{
	  stoppoint.i=i;
	  stoppoint.j=j+1;
	  way.push_back (stoppoint);
	  if (term[i][j+1]==0 || term[i][j+1]==color) term3[i][j+1]=color+2;
	  else term3[i][j+1]=color+3;
	  i=i;
	  j=j+1;
	  goto start;
	}
	if (j-1!=-1 && (term3[i][j-1]==color || term3[i][j-1]==color+1))
	{
	  stoppoint.i=i;
	  stoppoint.j=j-1;
	  way.push_back (stoppoint);
	  if (term[i][j-1]==0 || term[i][j-1]==color) term3[i][j-1]=color+2;
	  else term3[i][j-1]=color+3;
	  i=i;
	  j=j-1;
	  goto start;
	}
  }
  //создание пробоя, нужен для правильной работы функции
  holepoint.i=holepoint.j=holepoint.d=0;
  
  return holepoint;
}

bool alg (std::vector<std::vector<int>> &term, int n, int begin)
{
  long long int i,j,l,min,p1;
  ter_vitesse stoppoint;
  ter_way_min d_min;
  vector<vector<int>> term2 (n, vector<int>(n));
  vector<ter_vitesse> minway (n);
  vector<ter_vitesse> way (1);
  vector<ter_vitesse> waynew (1);
  vector<ter_way_min> way_dmin (0);
  vector<ter_way_min> way_coor (0); //вектор координат, куда произошла перестановка
  vector<int> opt (0); //вектор пути
  float G,R,L;//G - количество добавленных голубых, R - количество добавленных красных, L - общее количество добавленных
  float T=0;
  //float p;//вероятность совпадений
  term2=term;

  for (begin=0;begin<n;begin++)
	minway[begin]=deykstra (term, term2, n, 0, begin, 2);
  //поиск самого оптимального пути
  stoppoint.i=stoppoint.j=stoppoint.d=0;
  min=minway[0].d;
  for (i=1;i<n;i++)
	if (minway[i].d<min && minway[i].d>0)
	{
	  min=minway[i].d;
	  stoppoint=minway[i];
	}
  //отрисовка самого оптимального пути (кодовые цвета этого пути 4 и 5)
  way_opt (term, term2, way, n, stoppoint, 4);
  for (i=0;i<n;i++)
    for (j=0;j<n;j++)
	{
	  if (term2[i][j]<4 || term2[i][j]>5) term2[i][j]=term[i][j];
	  if (term2[i][j]==4 || term2[i][j]==5) opt.push_back(term[i][j]);
	}

  //поиск длины пути и количества добавленных
  L=way.size();
  if (p<=60) L=(0.059*p/L)+(L/n);
  else L=(L/n);
  R=0;
  for(i=0;i<way.size();i++)
	if (term[way[i].i][way[i].j]==0) R++;
    
  if (p<=60)
  {
	R=(R/n)-0.01*(p/L);
	if (R<0) R=0;
  }
  else R=(R/n);
  //создание изображения
  string nom=nom_des_images()+".bmp";
  vector<vector<ter_rgb>> term3 (n, vector<ter_rgb>(n));
  for (i=0;i<n;i++)
    for (j=0;j<n;j++)
	{
	  term3[i][j].r=term3[i][j].g=term3[i][j].b=255;

	  if (term2[i][j]==1)
		term3[i][j].r=term3[i][j].g=term3[i][j].b=0;

	  if (term2[i][j]==4)
	  {
		term3[i][j].r=255;
		term3[i][j].g=term3[i][j].b=0;
	  }

	  if (term2[i][j]==5)
	  {
		term3[i][j].r=127;
		term3[i][j].g=term3[i][j].b=0;
	  }
	}
  image (term3, n, nom);

  //поиск минимального расстояния для перестройки
  for (i=0;i<n;i++)
    for (j=0;j<n;j++)
      if (term2[i][j]==4)
	  {
		d_min=way_min (term, term2, n, i, j, 4);
		if (d_min.dmin==n*n+1) return true;
		way_dmin.push_back(d_min);
		//перестройка
		term2[d_min.i][d_min.j]=0;
		term2[i][j]=5;
		//запись координат
		d_min.i=i;
		d_min.j=j;
		way_coor.push_back(d_min);
	  }
  
/*
  //построение тепловой карты
  vector<vector<float>> term_termique (n, vector<float>(n));
  ter_way_min max_termique=carte_thermique (term, term_termique, n);
  float coef=255/max_termique.dmin;

  vector<vector<ter_rgb>> term4 (n, vector<ter_rgb>(n));
  for (i=0;i<n;i++)
    for (j=0;j<n;j++)
	{
	  term4[i][j].r=term_termique[i][j]*coef;
	  term4[i][j].g=0;
	  //if (term4[i][j].r>=207) term4[i][j].g=127;
	  term4[i][j].b=255;
	}
  term4[max_termique.i][max_termique.j].g=255;
  nom=nom_des_images()+" carte termique.bmp";
  image (term4, n, nom);
*/

  //запись статистических данных, координаты i и j - это координаты, откуда произошла перестановка
  /*ofstream f1 ("dmin i j beginx beginy.txt", ios::app);
  for (i=0;i<way_dmin.size();i++)
	f1<<way_dmin[i].dmin<<" "<<way_dmin[i].i<<" "<<way_dmin[i].j<<" "<<way_coor[i].i<<" "<<way_coor[i].j<<"\n";
  f1.close();*/

  //запись статистических данных по количеству добавленных и длине пути
  for (i=0;i<way_coor.size();i++)
	T+=way_coor[i].dmin;
  T=T/way_coor.size();
  if (R==0) T==0;

  ofstream f2 ("percolation.csv", ios::app);
  f2 << p << ";" << n << ";" << L << ";" << R << ";" << fixed << setprecision(5) << T << endl;
  f2.close();

  for (i=0;i<n;i++)
    for (j=0;j<n;j++)
	{
	  if (term2[i][j]>=1) term[i][j]=1;
	  else term[i][j]=0;
	}

  return true;
}

bool machine_a_cellules (std::vector<std::vector<int>> term, int n, int begin)
{
  std::vector< std::vector<int>> term2 (n, std::vector<int>(n));
  int vitesse=1;
  int i,j,p,v,error1,error2;
  bool flag=0;
l2:
  alg (term, n, begin);

  error1=error2=0;

  for (v=0;v<vitesse;v++)
    for (i=0;i<n;i++)
      for (j=0;j<n;j++)
		if (term[i][j]==1)
		{
		  error1++;
l3:
		  p=rand()%5;
		  if (p==1 && i-1>=0 && term2[i-1][j]==0)
		  {
			term2[i-1][j]=term[i][j];
			goto l1;
		  }
		  if (p==2 && j-1>=0 && term2[i][j-1]==0)
		  {
			term2[i][j-1]=term[i][j];
			goto l1;
		  }
		  if (p==3 && i+1<=n-1 && term2[i+1][j]==0)
		  {
			term2[i+1][j]=term[i][j];
			goto l1;
		  }
		  if (p==4 && j+1<=n-1 && term2[i][j+1]==0)
		  {
			term2[i][j+1]=term[i][j];
			goto l1;
		  }
		  if (term2[i][j]==0) term2[i][j]=term[i][j];
		  else
		  {
			if (flag==true) return false;
			flag=true;
			goto l3;
		  }
l1:
		  1+1;
		}
 
  for (i=0;i<n;i++)
    for (j=0;j<n;j++)
	{
	  if (term2[i][j]>=1)
	  {
		term[i][j]=1;
		error2++;
	  }
	  else term[i][j]=0;
	  term2[i][j]=0;
	}

  if (error1==error2) goto l2;

  return true;
}

unsigned long GetAppMemUsage()
{
 PROCESS_MEMORY_COUNTERS pmc;
 
 pmc.cb = sizeof(pmc);
 GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
 
 return pmc.WorkingSetSize;
}

int main(int argc, char *argv[])
{
  STARTUPINFO startupInfo ={0};
  startupInfo.cb = sizeof(startupInfo);
  PROCESS_INFORMATION processInformation;
  system("cls");
  char *Fileexe=argv[0];
  int L;//размер матрицы
  int i,j,t,step,step_i;
  bool flag;

  ifstream file("percolation.csv");
  string str, L_str, p_str;
  getline(file, str);
  getline(file, str);
  stringstream flux (str);
  getline (flux, p_str, ';');
  p=atoi(p_str.c_str());
  getline (flux, L_str, ';');
  L=atoi(L_str.c_str());
  file.close();

  srand(time(NULL));
  std::vector<vector<int>> term (L, std::vector<int>(L));
  //
  for(i=0;i<L;i++)
    for (j=0;j<L;j++)
	{
	  if (p>0 && (t=rand()%100)<=p) term[i][j]=1;
	  else term[i][j]=0;
	}
  //
  1+1;
  //flag=machine_a_cellules (term, L, j);
  flag=true;
  if (flag==true) alg (term, L, j);
  std::cout<<"fine!";

  Sleep(1000);
  CreateProcess(NULL,Fileexe,NULL,NULL,FALSE,0,NULL,NULL,&startupInfo,&processInformation);
  return 0;
}