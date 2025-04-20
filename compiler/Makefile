CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic -I..
LDFLAGS = -lstdc++fs

all: test_vm simple_test semicolon_test missing_semicolon_test vasuki_runner tail_optimization generate_bytecode

test_vm: test_vm.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o test_vm test_vm.cpp vasuki_vm.cpp $(LDFLAGS)

simple_test: simple_test.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o simple_test simple_test.cpp vasuki_vm.cpp $(LDFLAGS)

semicolon_test: semicolon_test.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o semicolon_test semicolon_test.cpp vasuki_vm.cpp $(LDFLAGS)

missing_semicolon_test: missing_semicolon_test.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o missing_semicolon_test missing_semicolon_test.cpp vasuki_vm.cpp $(LDFLAGS)

vasuki_runner: vasuki_runner.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o vasuki_runner vasuki_runner.cpp vasuki_vm.cpp $(LDFLAGS)

tail_optimization: tail_optimization.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o tail_optimization tail_optimization.cpp vasuki_vm.cpp $(LDFLAGS)

generate_bytecode: generate_bytecode.cpp vasuki_vm.cpp vasuki_vm.h
	$(CXX) $(CXXFLAGS) -o generate_bytecode generate_bytecode.cpp vasuki_vm.cpp $(LDFLAGS)

clean:
	rm -f test_vm simple_test semicolon_test missing_semicolon_test vasuki_runner tail_optimization generate_bytecode *.o *.bytecode

.PHONY: all clean
