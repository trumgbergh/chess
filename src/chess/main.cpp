#include<iostream>
#include<vector>

using namespace std;

int wp_dr[4] = {};
int wp_dc[4] = {};

struct CSquare
{
    int r; int c;

    CSquare(int r_ = -1, int c_ = -1) : r(r_), c(c_) {}
};

struct Trungbot
{
    Trungbot() {}

    void write(string& message)
    {
        cout << message << "\n";
        cout.flush();
        return;
    }

    bool valid_move(string& move)
    {
    }

    string read()
    {
        string response;
        cin >> response;
        return response;
    }
};

struct Board
{
    int turn;
    int castling;
    CSquare en_passant;
    vector<string> board;

    Board()
    {
        turn = 0;
        castling = 15;
        board = {"RNBQKBNR", "PPPPPPPP", "........", "........","........","........","pppppppp", "rnbqkbnr"};
    }

    void move_piece(CSquare u, CSquare v)
    {
        board[v.r][v.c] = board[u.r][u.c];
        board[u.r][u.c] = '.';
    }

    string gen_move()
    {
        return "0";
    }
};

int main()
{
    cout << "Trung bot running\n";
    Board b;
    while(true)
    {

    }
    return 0;
}
