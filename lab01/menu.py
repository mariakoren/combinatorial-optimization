from main import Graph

g = Graph()
g.load_from_file("file.txt")
g.draw_graph("basegraph")

def print_menu():
    print("Program przechowuje graf i pozwala na następujące operacji")
    print("1 - Dodanie krawędzi")
    print("2 - Usuwanie krawędzi")
    print("3 - Dodanie wierszchołka")
    print("4 - Usuwanie wierszchołka")
    print("5 - Wyznaczenie stopnia wierszchołka")
    print("6 - Wyznaczenie minimalnego stopnia grafu")
    print("7 - Wyznaczenie maksymalnego stopnia grafu")
    print("8 - Wyznaczenie ile wierszchołków jest stopnia parzystego i nieparzystego")
    print("9 - Wypisanie (posortowanego nierosnąco) ciągu stopni wierzchołków w grafie")
    print("0 - Wyjście")

def main():
    while True:
        print_menu()
        choose = int(input())

        if choose == 1:
            print("Między jakimi wierszchołkami dodać krawędź? Wprowadź 2 liczby")
            i = int(input())
            j = int(input())
            g.add_edge(i, j)
            print("Wprowadź nazwę pliku dla tego grafu")
            data = input()
            g.draw_graph(data)
        if choose == 2:
            print("Między jakimi wierszchołkami usunąć krawedź? Wprowadź 2 liczby")
            i = int(input())
            j = int(input())
            g.delete_edge(i, j)
            print("Wprowadź nazwę pliku dla tego grafu")
            data = input()
            g.draw_graph(data)
        if choose == 3:
            g.add_vertex()
            print("Wprowadź nazwę pliku dla tego grafu")
            data = input()
            g.draw_graph(data)
        if choose == 4:
            print("Jaki wierszchołek usunąć?")
            v = int(input())
            g.delete_vertex(v)
            print("Wprowadź nazwę pliku dla tego grafu")
            data = input()
            g.draw_graph(data)
        if choose == 5:
            print("Stopień jakiego wierszchołka trzeba wyznaczyć?")
            v = int(input())
            vd = g.vertex_degree(v)
            print(f"Stopień wierszchołka {v} wynosi {vd}")
        if choose == 6:
            mind = g.min_graph_degree()
            print(f"Minimalny stopień w grafie wynosi {mind}")
        if choose == 7:
            maxd = g.max_graph_degree()
            print(f"Maksymalny stopień w grafie wynosi {maxd}")
        if choose == 8:
            even, odd = g.even_odd_degrees()
            print(f"W podanym grafie {even} wierszchołków o parzystym stopniu")
            print(f"W podanym grafie {odd} wierszchołków o nieparzystym stopniu")
        if choose == 9:
            sorted = g.sorted_vertex_degrees()
            print(f"Stopni wierszchołków posortowane nierosnąco: {sorted}")
        if choose == 0:
            print("Koniec programu")
            break

main()







