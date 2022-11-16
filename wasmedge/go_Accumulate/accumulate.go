package main

import (
	"os"

	"github.com/second-state/WasmEdge-go/wasmedge"
)

func main() {
	// Set not to print debug info
	wasmedge.SetLogErrorLevel()

	// Create configure
	var conf = wasmedge.NewConfigure()
	conf.AddConfig(wasmedge.WASI)

	// Create VM with configure
	var vm = wasmedge.NewVMWithConfig(conf)

	// Init WASI (test)
	var wasi = vm.GetImportModule(wasmedge.WASI)
	wasi.InitWasi(
		os.Args[1:],  // The args
		os.Environ(), // The envs
		[]string{},   // The preopens will be empty
	)

	// Instantiate wasm
	vm.LoadWasmFile(os.Args[1])
	vm.Validate()
	vm.Instantiate()

	vm.Execute("acc")
	vm.Execute("acc")
	vm.Execute("acc")

	vm.Release()
	conf.Release()
}
