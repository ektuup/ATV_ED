#ifndef _RECENT_LIST_H_
#define _RECENT_LIST_H_

#define CUT_QUEUE 3

typedef struct{
    node* list;
    int len, len_max;
}RecentList;

RecentList* new_RecentList();
void list_add(RecentList* S, Pessoa p);
int in_list(RecentList* S, Priority pr);
void print_list(RecentList* S);
void delete_Recentlist(RecentList* S);

#endif