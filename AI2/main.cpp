#include <iostream>
#include<cmath>

using namespace std;
int X, Y;
#define MIN_SIZE 100000

char qi_pan[4][4], map[4][4];

struct step {
    int x;
    int y;
    double UCB;
    int visit;
    int win;
};
step set[14], *cur_set;

struct Chess {
    int x;
    int y;
    Chess *next;
    Chess *father;
    int th;
};

int check_1() {
    int i, j;
    int xa = 0, xb = 0;
    int ya = 0, yb = 0;
    for (i = 0; i < 4; i++) {
        int ra = 0, rb = 0;
        int ca = 0, cb = 0;
        if (qi_pan[i][i] == 'x')
            xa += 1;
        else if (qi_pan[i][i] == 'o')
            xb += 1;
        if (qi_pan[i][3 - i] == 'x')
            ya += 1;
        else if (qi_pan[i][3 - i] == 'o')
            yb += 1;
        for (j = 0; j < 4; j++) {
            if (qi_pan[i][j] == 'x')
                ra += 1;
            else if (qi_pan[i][j] == 'o')
                rb += 1;
            if (qi_pan[j][i] == 'x')
                ca += 1;
            else if (qi_pan[j][i] == 'o')
                cb += 1;
        }
        if (ra == 4 || ca == 4 || xa == 4 || ya == 4)
            return 1;
        else if (rb == 4 || cb == 4 || xb == 4 || yb == 4)
            return 0;
    }
    return -1;
}

int check() {
    int i, j;
    int xa = 0, xb = 0;
    int ya = 0, yb = 0;
    for (i = 0; i < 4; i++) {
        int ra = 0, rb = 0;
        int ca = 0, cb = 0;
        if (map[i][i] == 'x')
            xa += 1;
        else if (map[i][i] == 'o')
            xb += 1;
        if (map[i][3 - i] == 'x')
            ya += 1;
        else if (map[i][3 - i] == 'o')
            yb += 1;
        for (j = 0; j < 4; j++) {
            if (map[i][j] == 'x')
                ra += 1;
            else if (map[i][j] == 'o')
                rb += 1;
            if (map[j][i] == 'x')
                ca += 1;
            else if (map[j][i] == 'o')
                cb += 1;
        }
        if (ra == 4 || ca == 4 || xa == 4 || ya == 4) {
            return 1;
        } else if (rb == 4 || cb == 4 || xb == 4 || yb == 4) {
            return 0;
        }
    }
    return -1;
}

int MCT(int sum, int player) {
    Chess *head, *cur, *temp;
    int th = 0, random_chess;
    temp = (Chess *) malloc(sizeof(Chess));
    head = temp;
    temp->father = nullptr;

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (map[i][j] == ' ') {
                cur = (Chess *) malloc(sizeof(Chess));
                cur->th = th++;
                cur->next = nullptr;
                cur->x = i;
                cur->y = j;
                temp->next = cur;
                cur->father = temp;
                temp = cur;
            }//建立空棋位链表
        }
    }
    head = head->next;//吃掉第一个空的头
    free(head->next);
    head->next = nullptr;
    while (head != nullptr) {
        srand(time(nullptr));
        random_chess = rand() % sum;//生成一个随机数来随机下一个棋子，这个sum是递减的，随机数生成范围会根据可下棋的空位数减少而减少

        if (head->next == nullptr) {
            cur = head;
            head = nullptr;
            goto b;
        }//如果只剩最后一个位子可以下，直接跳转判断
        if (head->th == random_chess) {
            head->next->father = nullptr;
            cur = head;
            head = head->next;

            while (cur != nullptr) {
                cur->th -= 1;
                cur = cur->next;
            }
            cur = head;
            goto b;
        }//如果刚好随机数生成为0则取头节点，但头节点没有father节点，属于特殊情况拿了出来
        cur = head;
        while (cur != nullptr) {
            if (cur->th == random_chess) {
                if (cur->next != nullptr) {
                    cur->next->father = cur->father;
                }
                cur->father->next = cur->next;
                temp = cur->next;
                while (temp != nullptr) {
                    temp->th -= 1;
                    temp = temp->next;
                }
                break;
            } else
                cur = cur->next;
        }//从链表里面找到随机数对应的序号的那个棋位下上棋子

        b:
        if (player & 1) {
            map[cur->x][cur->y] = 'x';
            free(cur);
        }//player是1的时候归人下，人执x
        else {
            map[cur->x][cur->y] = 'o';
            free(cur);
        }//player是0归电脑下
        if (check() != -1) {
            return check();//胜负出现了就直接返回了
        }
        player = 1 - player;//换手
        sum--;//缩小随机数范围
    }
    return check();//head==null了，没棋可下了。
}

void cal1(step *set1, int sum) {

    while (set1->visit < MIN_SIZE) {
        if (MCT(sum, 1) == 0) {
            set1->visit++;
            set1->win++;
        } else {
            set1->visit++;
        }
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                map[i][j] = qi_pan[i][j];
            }
        }
        map[set1->x][set1->y] = 'o';
    }
}

void MCT_once(step *, int sum) {
}

step *Foundmax(int sum) {
    step *wow;
    wow = (step *) malloc(sizeof(step));
    wow->UCB = 0;
    for (int i = 0; i < sum; i++) {
        if (wow->UCB < set[i].UCB) {
            wow = &set[i];
        }
    }
    return wow;
}

int main() {
    clock_t start, finish;
    int totalvisit = 0;

    int sum = 14;
    int x, y;
    double TheTimes;

    int s = 0;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            qi_pan[i][j] = ' ';
            map[i][j] = ' ';
        }
    }
    while (check_1() == -1) {
        printf("your turn:");
        scanf("%d %d", &x, &y);
        start = clock();
        qi_pan[x][y] = 'x';
        map[x][y] = 'x';
        for (int i = 0; i < sum; i++) {
            set[i].visit = 0;
            set[i].win = 0;
        }
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {

                if (map[i][j] == ' ') {
                    set[s].x = i;
                    set[s].y = j;
                    map[i][j]='x';
                    if (check()==1) {
                        cur_set=&set[s];
                        goto c;
                    }
                    map[i][j] = 'o';

                    if (check()==0) {
                        cur_set=&set[s];
                        goto c;
                    }
                    cal1(&set[s++], sum);
                    for (int i1 = 0; i1 < 4; i1++)
                        for (int j1 = 0; j1 < 4; j1++)
                            map[i1][j1] = qi_pan[i1][j1];
                }
            }
        }

        while (true) {
            a:
            finish = clock();
            TheTimes = (double) ((finish - start) / CLOCKS_PER_SEC);
            if (TheTimes >= 5) {
                break;
            }
            for (int i = 0; i < sum; i++) {
                totalvisit += set[i].visit;
                set[i].UCB = set[i].win / set[i].visit + sqrt(2 * log(totalvisit) / set[i].visit);
            }
            cur_set = Foundmax(sum);
            MCT_once(cur_set, sum);
            goto a;
        }
        cur_set = Foundmax(sum);
        c:qi_pan[cur_set->x][cur_set->y] = 'o';
        map[cur_set->x][cur_set->y] = 'o';
        printf("SK chose (%d,%d)\n", cur_set->x, cur_set->y);
        for (int x=0; x<4; x++) {
            for (int y=0; y<4; y++) {
                printf ("%c", qi_pan[x][y]);
            }
            printf ("\n");
        }
        s = 0;
        sum -= 2;

    }

    return 0;
}