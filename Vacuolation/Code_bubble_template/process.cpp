#include <bits/stdc++.h>
using namespace std;

#define DEBUG 0
#define PI 3.141592653589

int n = 3024, process_id;
int brightness[3500][3500];
int Out_R[3500][3500], Out_G[3500][3500], Out_B[3500][3500];
int seg[3500][3500];
int tmp[3500 * 3500], tmpcnt;

void read_file(int arr[3500][3500], const char* file)
{
	FILE* fin = fopen(file, "r");
	for (int i = 1; i <= n; i++)
		for (int j = 1; j <= n; j++)
			fscanf(fin, "%d", &arr[i][j]);
	fclose(fin);
}

int CellCnt, Cell_Circle_Cnt[5010], Area[5010], Cell_Circles[5010][2010];

void read_files()
{
	char infile[30] = {};

	if (DEBUG) printf("Read brightness image\n");
	sprintf(infile, "./tmp/tmp_%d/in_1.txt", process_id);
	read_file(brightness, infile);

	if (DEBUG) printf("Read segmentation image\n");
	sprintf(infile, "./tmp/tmp_%d/in_2.txt", process_id);
	read_file(seg, infile);
	
	if (DEBUG) printf("Read finished\n");
}

int Queue[3500 * 3500][2], head, tail;
int Queue2[3500 * 3500][2], head2, tail2;
int vis[3500][3500], CellId[3500][3500];
const int inf = 1000000000;

int get_percentile(int arr[], int nid, double percentile, bool needsort)
{
    int k = round(nid * percentile / 100);
	k = min(max(k, 1), nid);
	if (needsort) sort(arr + 1, arr + nid + 1);
	return arr[k];
}

void process_cells()
{
	// vis: 0 unvisited; 1 visited; 2 checked for bubble
	for (int x = 1; x <= n; x++)
		for (int y = 1; y <= n; y++)
			vis[x][y] = 0;
	int detection = 0;
	for (int x = 1; x <= n; x++) for (int y = 1; y <= n; y++)
	{
		if (vis[x][y] != 0) continue;
		if (seg[x][y] == 0) continue;
		vis[x][y] = 1;
		Queue[1][0] = x;
		Queue[1][1] = y;
		head = tail = 1;
		while (head <= tail)
		{
			int cur_x = Queue[head][0], cur_y = Queue[head][1];
			head += 1;
			for (int add_x = -1; add_x <= 1; add_x++)
				for (int add_y = -1; add_y <= 1; add_y++)
				{
					int next_x = cur_x + add_x;
					int next_y = cur_y + add_y;
					if (!(1 <= next_x && next_x <= n)) continue;
					if (!(1 <= next_y && next_y <= n)) continue;
					if (seg[next_x][next_y] != seg[cur_x][cur_y]) continue;
					if (vis[next_x][next_y] == 0)
					{
						vis[next_x][next_y] = 1;
						tail += 1;
						Queue[tail][0] = next_x;
						Queue[tail][1] = next_y;
					}
				}
		}
		// printf("tail %d\n", tail);
		detection += 1;
		// filter out cells too small
		if (tail <= 5000)
			continue;
		
		// flag all the area as a new cell
		CellCnt += 1;
		Area[CellCnt] = tail;
		for (int k = 1; k <= tail; k++)
		{
			int cur_x = Queue[k][0], cur_y = Queue[k][1];
			CellId[cur_x][cur_y] = CellCnt;
		}

		// flag all the new cell to white (for debug segmentation purpose)
//		for (int k = 1; k <= tail; k++)
//		{
//			int cur_x = Queue[k][0], cur_y = Queue[k][1];
//			Out_R[cur_x][cur_y] = Out_G[cur_x][cur_y] = Out_B[cur_x][cur_y] = 255;
//		}

		// threshold the cell by percentile
		tmpcnt = 0;
		for (int k = 1; k <= tail; k++)
		{
			int cur_x = Queue[k][0], cur_y = Queue[k][1];
			tmp[++tmpcnt] = brightness[cur_x][cur_y];
		}
		int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 30;
//		int percentile_value = get_percentile(tmp, tmpcnt, 60, true);
//		int mini = get_percentile(tmp, tmpcnt, 5, false);
//		int maxi = get_percentile(tmp, tmpcnt, 40, false);
//		percentile_value = percentile_value + (maxi - mini) * 1.5;

		// record the threshold to output
		for (int k = 1; k <= tail; k++) 
		{
			int cur_x = Queue[k][0], cur_y = Queue[k][1];
			if (brightness[cur_x][cur_y] >= percentile_value) // white
				Out_R[cur_x][cur_y] = Out_G[cur_x][cur_y] = Out_B[cur_x][cur_y] = 255;
			else // gray
				Out_R[cur_x][cur_y] = Out_G[cur_x][cur_y] = Out_B[cur_x][cur_y] = 128;
		}

		// locate the bright areas
		for (int k = 1; k <= tail; k++)
		{
			int cur_x = Queue[k][0], cur_y = Queue[k][1];
			if (brightness[cur_x][cur_y] < percentile_value) continue;
			vis[cur_x][cur_y] = 2;
			Queue2[1][0] = cur_x;
			Queue2[1][1] = cur_y;
			head2 = tail2 = 1;
			while (head2 <= tail2)
			{
				int cur_x2 = Queue2[head2][0], cur_y2 = Queue2[head2][1];
				head2 += 1;
				for (int add_x = -1; add_x <= 1; add_x++)
					for (int add_y = -1; add_y <= 1; add_y++)
					{
						int next_x = cur_x2 + add_x;
						int next_y = cur_y2 + add_y;
						if (!(1 <= next_x && next_x <= n)) continue;
						if (!(1 <= next_y && next_y <= n)) continue;
						if (seg[next_x][next_y] != seg[cur_x2][cur_y2]) continue;
						if (brightness[next_x][next_y] < percentile_value) continue;
						if (vis[next_x][next_y] == 1)
						{
							vis[next_x][next_y] = 2;
							tail2 += 1;
							Queue2[tail2][0] = next_x;
							Queue2[tail2][1] = next_y;
						}
					}
			}
			// filter the bubbles too small or too large
			if (tail2 < 10 || tail2 > tail * 0.85) continue;

			// check whether this bubble touches another cell or image boundary
			// if yes, filter this bubble
			bool Touch_boundary = false;
			for (int k2 = 1; k2 <= tail2 && Touch_boundary == false; k2++)
			{
				int cur_x2 = Queue2[k2][0], cur_y2 = Queue2[k2][1];
				for (int add_x = -1; add_x <= 1 && Touch_boundary == false; add_x++)
					for (int add_y = -1; add_y <= 1 && Touch_boundary == false; add_y++)
					{
						int next_x = cur_x2 + add_x;
						int next_y = cur_y2 + add_y;
						if (!(1 <= next_x && next_x <= n)) { Touch_boundary = true; continue; }
						if (!(1 <= next_y && next_y <= n)) { Touch_boundary = true; continue; }
						if (seg[next_x][next_y] != seg[cur_x2][cur_y2])
							Touch_boundary = true;
					}
			}
			if (Touch_boundary == true)
				continue;

			// check whether this area is a bubble by circularity estimation
			int perimeter = 0;
			for (int k2 = 1; k2 <= tail2; k2++)
			{
				int cur_x2 = Queue2[k2][0], cur_y2 = Queue2[k2][1];

				bool Is_boundary = false;
                if (vis[cur_x2 - 1][cur_y2] == 1) Is_boundary = true; // up
                else if (vis[cur_x2 + 1][cur_y2] == 1) Is_boundary = true; // down
                else if (vis[cur_x2][cur_y2 - 1] == 1) Is_boundary = true; // left
                else if (vis[cur_x2][cur_y2 + 1] == 1) Is_boundary = true; // right
				if (Is_boundary == true) perimeter++;
			}
			double circularity = 4 * PI * tail2 / (perimeter * perimeter);

			if (circularity < 0.6)
			{
				// draw the wrong bubbles for debug
				for (int k2 = 1; k2 <= tail2; k2++)
				{
					int cur_x2 = Queue2[k2][0], cur_y2 = Queue2[k2][1];

					bool Is_boundary = false;
					if (vis[cur_x2 - 1][cur_y2] == 1) Is_boundary = true; // up
					else if (vis[cur_x2 + 1][cur_y2] == 1) Is_boundary = true; // down
					else if (vis[cur_x2][cur_y2 - 1] == 1) Is_boundary = true; // left
					else if (vis[cur_x2][cur_y2 + 1] == 1) Is_boundary = true; // right
					if (Is_boundary == true)
					{
						Out_R[cur_x2][cur_y2] = 255;
						Out_G[cur_x2][cur_y2] = Out_B[cur_x2][cur_y2] = 0;
					}
				}
			}
			else
			{
				// record the bubble
				int cur_CellId = CellId[cur_x][cur_y];
				int cur_CircleId = ++Cell_Circle_Cnt[cur_CellId];
				Cell_Circles[cur_CellId][cur_CircleId] = tail2;
				
				// draw the correct bubbles
				for (int k2 = 1; k2 <= tail2; k2++)
				{
					int cur_x2 = Queue2[k2][0], cur_y2 = Queue2[k2][1];

					bool Is_boundary = false;
					if (vis[cur_x2 - 1][cur_y2] == 1) Is_boundary = true; // up
					else if (vis[cur_x2 + 1][cur_y2] == 1) Is_boundary = true; // down
					else if (vis[cur_x2][cur_y2 - 1] == 1) Is_boundary = true; // left
					else if (vis[cur_x2][cur_y2 + 1] == 1) Is_boundary = true; // right
					if (Is_boundary == true)
					{
						Out_G[cur_x2][cur_y2] = 255;
						Out_R[cur_x2][cur_y2] = Out_B[cur_x2][cur_y2] = 0;
					}
				}
			}
		}
	}
//	printf("CellCnt %d\n", CellCnt);
//	printf("Detection %d\n", detection);
}


char sout[3500 * 3500 * 8]; int sout_tot;
void print(int x)
{
	if(x>9)
	{
		print(x/10);
		sout[sout_tot++] = x%10+'0';
	}
	else
		sout[sout_tot++] = x+'0';
	return; 
}

void write_file(int arr[3500][3500], const char* file)
{
	sout_tot = 0;
	memset(sout, 0, sizeof(sout));
	FILE* fout = fopen(file, "w");
	for (int i = 1; i <= n; i++)
	{
		for (int j = 1; j <= n; j++)
		{
			print(arr[i][j]);
			sout[sout_tot++]=' ';
		}
		sout[sout_tot++]='\n';
	}
	fprintf(fout, "%s", sout);
	fclose(fout);
}

void write_results()
{
    // write image output
	char outfile[30] = {};
	sprintf(outfile, "./tmp/tmp_%d/out_r.txt", process_id);
	write_file(Out_R, outfile);
	sprintf(outfile, "./tmp/tmp_%d/out_g.txt", process_id);
	write_file(Out_G, outfile);
	sprintf(outfile, "./tmp/tmp_%d/out_b.txt", process_id);
	write_file(Out_B, outfile);

	// write results for visualization / quantification
	sprintf(outfile, "./tmp/tmp_%d/result.txt", process_id);
	FILE* fout = fopen(outfile, "w");

	for (int i = 1; i <= CellCnt; i++)
	{
		fprintf(fout, "%d %d\n", Cell_Circle_Cnt[i], Area[i]);
		for (int j = 1; j <= Cell_Circle_Cnt[i]; j++)
			fprintf(fout, "%d\n", Cell_Circles[i][j]);
	}
    fclose(fout);
}

int main(int argc, char **argv)
{
	sscanf(argv[1], "%d", &process_id);
	
	// step 1: read files
	if (DEBUG) printf("=====Step 1=====\n");
	read_files();

	// step 2: for each cell, check bubbles
	if (DEBUG) printf("=====Step 2=====\n");
	process_cells();

	// step 3: write results
	if (DEBUG) printf("=====Step 3=====\n");
	write_results();
	
	if (DEBUG) printf("=====C++ Done=====\n");
	return 0;
}
