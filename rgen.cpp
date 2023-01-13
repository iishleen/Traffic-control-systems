#include <iostream>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <math.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <algorithm>
#include <regex>

using namespace std;

unsigned int init_rand()
{
    unsigned int rNum = 0;
    ifstream urandom("/dev/urandom", ios::in | ios::binary);

    if (urandom.fail())
    {
        cerr << "Error: /dev/urandom cannot be opened\n";
        return 1;
    }
    urandom.read((char *)&rNum, 1);
    urandom.close();
    return rNum;
}

int get_random_num(unsigned int rNew, int x, int y)
{
    int rNum = round((((float)rNew / 255)) * (float)(y - x)) + x;
    return rNum;
}

bool if_bound_seg(vector<int> point3, vector<int> point4, vector<int> point2)
{
    if ((point2[0] <= max(point3[0], point4[0])) && (point2[0] >= min(point3[0], point4[0])) && (point2[1] <= max(point3[1], point4[1])) && (point2[1] >= min(point3[1], point4[1])))
        return true;
    return false;
}

bool if_overlapping(vector<int> point1, vector<int> point2, vector<int> point3, vector<int> point4)
{
    if ((max(point1[0], point2[0]) < min(point3[0], point4[0])) || (min(point1[0], point2[0]) > max(point3[0], point4[0])) || (max(point1[1], point2[1]) < min(point3[1], point4[1])) || (min(point1[1], point2[1]) > max(point3[1], point4[1])))
        return false;
    else
    {
        int x1 = point1[1] - point2[1];
        int y1 = point2[0] - point1[0];
        int x2 = point3[1] - point4[1];
        int y2 = point4[0] - point3[0];

        int det = x1 * y2 - y1 * x2;

        int tp1 = (point3[0] - point1[0]) * (point2[1] - point4[1]) - (point2[0] - point4[0]) * (point3[1] - point1[1]);
        int tp2 = (point4[0] - point1[0]) * (point3[1] - point2[1]) - (point3[0] - point2[0]) * (point4[1] - point1[1]);
        if (det == 0 && tp1 == 0 && tp2 == 0)
        {
            int tp3 = (point2[0] - point1[0]) * (point3[1] - point4[1]) - (point3[0] - point4[0]) * (point2[1] - point1[1]);
            int tp4 = (point4[0] - point1[0]) * (point2[1] - point3[1]) - (point2[0] - point3[0]) * (point4[1] - point1[1]);
            if (tp3 == 0 && tp4 == 0)
            {
                if (((((point2[0] == point3[0]) && (point2[1] == point3[1])) && (!if_bound_seg(point1, point2, point4))) || ((!if_bound_seg(point1, point2, point3)) && ((point2[0] == point4[0]) && (point2[1] == point4[1])))))
                    return false;
                else
                    return true;
            }
            else
                return false;
        }
        if (det != 0)
            return false;
        else
            return false;
    }
    return false;
}

bool overlap_check(int x2, int y2, vector<vector<int>> strs, vector<int> sgms, int id)
{
    if (id > 0)
    {
        vector<int> point2;
        point2.push_back(x2);
        point2.push_back(y2);
        int x1 = sgms[sgms.size() - 2];
        int y1 = sgms[sgms.size() - 1];
        vector<int> point1;
        point1.push_back(x1);
        point1.push_back(y1);
        vector<int> old_str;
        vector<int> point4;
        vector<int> point3;
        int x3;
        int x4;
        int y3;
        int y4;

        for (int s = 0; s < id; ++s)
        {
            old_str.clear();
            old_str = strs[s];
            for (unsigned int i = 0; i < (old_str.size() - 2); i = i + 2)
            {
                x3 = old_str[i];
                x4 = old_str[i + 2];
                y3 = old_str[i + 1];
                y4 = old_str[i + 3];
                point3.clear();
                point4.clear();
                point3.push_back(x3);
                point3.push_back(y3);
                point4.push_back(x4);
                point4.push_back(y4);
                if (if_overlapping(point1, point2, point3, point4))
                    return true;
                else
                    continue;
            }
        }
    }
    else
        return false;
    return false;
}

bool if_intersecting(vector<int> point1, vector<int> point2, vector<int> point3, vector<int> point4)
{
    if ((max(point1[0], point2[0]) < min(point3[0], point4[0])) || (min(point1[0], point2[0]) > max(point3[0], point4[0])) || (max(point1[1], point2[1]) < min(point3[1], point4[1])) || (min(point1[1], point2[1]) > max(point3[1], point4[1])))
        return false;
    else
    {
        int x1 = point1[1] - point2[1];
        int x2 = point3[1] - point4[1];
        int y1 = point2[0] - point1[0];
        int y2 = point4[0] - point3[0];
        int z1 = point2[0] * point1[1] - point1[0] * point2[1];
        int z2 = point4[0] * point3[1] - point3[0] * point4[1];

        int det = x1 * y2 - y1 * x2;
        int det_x = z1 * y2 - y1 * z2;
        int det_y = x1 * z2 - z1 * x2;

        int tp1 = (point3[0] - point1[0]) * (point2[1] - point4[1]) - (point2[0] - point4[0]) * (point3[1] - point1[1]);
        int tp2 = (point4[0] - point1[0]) * (point3[1] - point2[1]) - (point3[0] - point2[0]) * (point4[1] - point1[1]);
        if (det == 0 && tp1 == 0 && tp2 == 0)
        {
            int tp3 = (point2[0] - point1[0]) * (point3[1] - point4[1]) - (point3[0] - point4[0]) * (point2[1] - point1[1]);
            int tp4 = (point4[0] - point1[0]) * (point2[1] - point3[1]) - (point2[0] - point3[0]) * (point4[1] - point1[1]);
            if (tp3 == 0 && tp4 == 0)
            {
                if ((point4[0] == point1[0] && point4[1] == point1[1]) && !if_bound_seg(point3, point4, point2))
                    return false;

                else
                    return true;
            }
            else
                return false;
        }
        if (det != 0)
        {
            float X = (float)det_x / (float)det;
            float Y = (float)det_y / (float)det;
            if ((X < (max(min(point1[0], point2[0]), min(point3[0], point4[0])))) || (X > (min(max(point1[0], point2[0]), max(point3[0], point4[0])))) || (Y < (max(min(point1[1], point2[1]), min(point3[1], point4[1])))) || (Y > (min(max(point1[1], point2[1]), max(point3[1], point4[1])))))
                return false;
            else
            {
                if ((point4[0] == point1[0] && point4[1] == point1[1]))
                    return false;
                else
                    return true;
            }
        }
        else
            return false;
    }
    return false;
}

bool intersect_check(int x2, int y2, vector<int> sgms)
{
    vector<int> point2;
    point2.push_back(x2);
    point2.push_back(y2);
    for (unsigned int i = 0; i < sgms.size(); i = i + 2)
        if (x2 == sgms[i] && y2 == sgms[i + 1])
            return true;
    int x1 = sgms[sgms.size() - 2];
    int y1 = sgms[sgms.size() - 1];
    vector<int> point1;
    point1.push_back(x1);
    point1.push_back(y1);
    vector<int> point3;
    vector<int> point4;
    int x3;
    int x4;
    int y3;
    int y4;

    for (unsigned int i = 0; i < (sgms.size() - 2); i = i + 2)
    {
        x3 = sgms[i];
        y3 = sgms[i + 1];
        x4 = sgms[i + 2];
        y4 = sgms[i + 3];
        point3.clear();
        point4.clear();
        point3.push_back(x3);
        point3.push_back(y3);
        point4.push_back(x4);
        point4.push_back(y4);

        if (if_intersecting(point1, point2, point3, point4))
            return true;
        else
            continue;
    }
    return false;
}

vector<int> segment_gen(vector<vector<int>> strs, vector<int> sgms, int id, int max_coords)
{
    vector<int> pts;
    unsigned int randx2 = init_rand();
    unsigned int randy2 = init_rand();
    int x2 = get_random_num(randx2, -max_coords, max_coords);
    int y2 = get_random_num(randy2, -max_coords, max_coords);
    if (sgms.size() == 0)
    {
        pts.push_back(x2);
        pts.push_back(y2);
        return (pts);
    }
    else if (sgms.size() == 2)
    {
        if (sgms[0] != x2 || sgms[1] != y2)
        {
            if (!overlap_check(x2, y2, strs, sgms, id))
            {
                pts.push_back(x2);
                pts.push_back(y2);
                return (pts);
            }
        }
    }
    else
    {
        if (!overlap_check(x2, y2, strs, sgms, id) && !intersect_check(x2, y2, sgms))
        {
            pts.push_back(x2);
            pts.push_back(y2);
            return (pts);
        }
    }
    return (pts);
}

char num_to_char(int a)
{
    return static_cast<char>('A' + a);
}

bool existing_intersect(vector<vector<int>> strs)
{
    vector<int> point1;
    vector<int> point2;
    vector<int> point3;
    vector<int> point4;
    for (size_t i = 0; i < (strs.size() - 1); ++i)
    {
        for (size_t j = i + 1; j < strs.size(); ++j)
        {
            for (size_t m = 0; m < (strs[i].size() - 2); m = m + 2)
            {
                point1.clear();
                point2.clear();
                point1.push_back(strs[i][m]);
                point1.push_back(strs[i][m + 1]);
                point2.push_back(strs[i][m + 2]);
                point2.push_back(strs[i][m + 3]);
                for (size_t n = 0; n < (strs[j].size() - 2); n = n + 2)
                {
                    point3.clear();
                    point4.clear();
                    point3.push_back(strs[j][n]);
                    point3.push_back(strs[j][n + 1]);
                    point4.push_back(strs[j][n + 2]);
                    point4.push_back(strs[j][n + 3]);
                    if (point4[0] == point1[0] && point4[1] == point1[1])
                        return true;
                    else
                    {
                        bool fl = (if_intersecting(point1, point2, point3, point4));
                        if (fl == true)
                            return fl;
                        else
                            continue;
                    }
                }
            }
        }
    }
    return false;
}

int main(int argc, char **argv)
{
    int streets_num = 10;
    int l_segments = 5;
    int waiting_time = 5;
    int max_coords = 20;
    int c;
    int c_num = 0;

    int numstreets;
    int wait_time;
    opterr = 0;

    while ((c = getopt(argc, argv, "s:n:l:c:")) != -1)
        switch (c)
        {
        case 's':
            streets_num = atoi(optarg);
            if ((streets_num >= 2))
                break;
            else
            {
                cerr << "Error: Invalid parameter for option -s" << endl;
                return 1;
            }
        case 'n':
            l_segments = atoi(optarg);
            if ((l_segments >= 1))
                break;
            else
            {
                cerr << "Error: Invalid parameter for option -n" << endl;
                return 1;
            }
        case 'l':
            waiting_time = atoi(optarg);
            if ((waiting_time >= 5))
                break;
            else
            {
                cerr << "Error: Invalid parameter for option -l" << endl;
                return 1;
            }
        case 'c':
            max_coords = atoi(optarg);
            if ((max_coords >= 1))
                break;
            else
            {
                cerr << "Error: Invalid parameter for option -c" << endl;
                return 1;
            }
        case '?':
            if (optopt == 's')
            {
                cerr << "Error: No argument provided for option -s" << endl;
                return 1;
            }

            else if (optopt == 'n')
            {
                cerr << "Error: No argument provided for option -n" << endl;
                return 1;
            }

            else if (optopt == 'l')
            {
                cerr << "Error: No argument provided for option -l" << endl;
                return 1;
            }

            else if (optopt == 'c')
            {
                cerr << "Error: No argument provided for option -c" << endl;
                return 1;
            }
            else
            {
                cerr << "Error: This option is invalid! " << endl;
                return 1;
            }
        default:
            return 0;
        }
    while (!cin.eof())
    {
        unsigned int rand = init_rand();
        numstreets = get_random_num(rand, 2, streets_num);
        vector<vector<int>> strs;
        vector<string> nms;
        for (int i = 0; i < numstreets; ++i)
        {
            unsigned int rand = init_rand();
            int l_segments_num = get_random_num(rand, 1, l_segments);
            vector<int> sgms;
            for (int j = 0; j < (l_segments_num + 1); ++j)
            {
                c_num = 0;
                while (c_num < 25)
                {
                    vector<int> pts = segment_gen(strs, sgms, i, max_coords);
                    if (pts.size() > 0)
                    {
                        if ((i == (numstreets - 1)) && (j == (l_segments_num)))
                        {
                            sgms.push_back(pts[0]);
                            sgms.push_back(pts[1]);
                            strs.push_back(sgms);
                            if (existing_intersect(strs))
                            {
                                strs.pop_back();
                                break;
                            }
                            else
                            {
                                strs.pop_back();
                                sgms.pop_back();
                                sgms.pop_back();
                            }
                        }
                        else
                        {
                            sgms.push_back(pts[0]);
                            sgms.push_back(pts[1]);
                            break;
                        }
                    }
                    c_num = c_num + 1;
                }
                if (c_num >= 25)
                {
                    cerr << "Error: Unable to generate specification after 25 attempts" << endl;
                    return (1);
                }
                else
                    continue;
            }
            string out;
            for (size_t m = 0; m < sgms.size(); m = m + 2)
            {
                out.append("(");
                out.append(to_string(sgms[m]));
                out.append(",");
                out.append(to_string(sgms[m + 1]));
                if ((m + 1) != sgms.size() - 1)
                    out.append(") ");
                else
                    out.append(")");
            }
            string sletter(1, num_to_char(i));
            string str_name = "\"Street" + sletter + "\" ";
            nms.push_back(str_name);
            cout << "add " << str_name << out << endl;
            out.clear();
            strs.push_back(sgms);
            sgms.clear();
        }
        cout << "gg" << endl;

        unsigned int wait = init_rand();
        wait_time = get_random_num(wait, 5, waiting_time);
        sleep(wait_time);

        for (size_t n = 0; n < nms.size(); ++n)
            cout << "rm " << nms[n] << endl;
        nms.clear();
    }
    return 0;
}