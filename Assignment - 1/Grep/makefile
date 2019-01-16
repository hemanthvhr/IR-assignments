search: searcher.cpp present
	g++ -std=c++11 -o search searcher.cpp
present: presenter.cpp
	g++ -std=c++11 -o present presenter.cpp
clean:
	rm results.txt performance.txt search present
run:
	make search
	./search < query.txt > performance.txt
