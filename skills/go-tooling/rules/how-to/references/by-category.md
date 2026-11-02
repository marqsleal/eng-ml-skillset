# Golang skills — full catalog by category

42 skills. Skills marked ⭐️ are recommended for all Go projects. Skills marked ⚙️ can be superseded by a company-specific skill.

---

## Table of Contents

- [Code Quality](#code-quality)
  - [[golang-code-style](../../../../go-coding-standards/rules/code-style/guide.md) ⭐️ ⚙️](#sambercc-skills-golanggolang-code-style-%EF%B8%8F-%EF%B8%8F)
  - [[golang-documentation](../../../../go-coding-standards/rules/documentation/guide.md) ⭐️ ⚙️](#sambercc-skills-golanggolang-documentation-%EF%B8%8F-%EF%B8%8F)
  - [[golang-error-handling](../../../../go-coding-standards/rules/error-handling/guide.md) ⭐️ ⚙️](#sambercc-skills-golanggolang-error-handling-%EF%B8%8F-%EF%B8%8F)
  - [[golang-lint](../../lint/guide.md)](#sambercc-skills-golanggolang-lint)
  - [[golang-naming](../../../../go-coding-standards/rules/naming/guide.md) ⭐️ ⚙️](#sambercc-skills-golanggolang-naming-%EF%B8%8F-%EF%B8%8F)
  - [[golang-safety](../../../../go-coding-standards/rules/safety/guide.md) ⭐️](#sambercc-skills-golanggolang-safety-%EF%B8%8F)
  - [[golang-security](../../../../go-web-application/rules/security/guide.md) ⭐️ 🧠](#sambercc-skills-golanggolang-security-%EF%B8%8F-)
  - [[golang-structs-interfaces](../../../../go-coding-standards/rules/structs-interfaces/guide.md) ⚙️](#sambercc-skills-golanggolang-structs-interfaces-%EF%B8%8F)
- [Architecture & Design](#architecture--design)
  - [[golang-concurrency](../../../../go-coding-standards/rules/concurrency/guide.md) ⚙️](#sambercc-skills-golanggolang-concurrency-%EF%B8%8F)
  - [[golang-context](../../../../go-coding-standards/rules/context/guide.md) ⚙️](#sambercc-skills-golanggolang-context-%EF%B8%8F)
  - [[golang-data-structures](../../../../go-coding-standards/rules/data-structures/guide.md) ⭐️](#sambercc-skills-golanggolang-data-structures-%EF%B8%8F)
  - [[golang-database](../../../../go-web-application/rules/database/guide.md) ⭐️ ⚙️](#sambercc-skills-golanggolang-database-%EF%B8%8F-%EF%B8%8F)
  - [[golang-dependency-injection](../../../../go-coding-standards/rules/dependency-injection/guide.md) ⚙️](#sambercc-skills-golanggolang-dependency-injection-%EF%B8%8F)
  - [[golang-design-patterns](../../../../go-coding-standards/rules/design-patterns/guide.md) ⭐️ ⚙️](#sambercc-skills-golanggolang-design-patterns-%EF%B8%8F-%EF%B8%8F)
  - [[golang-modernize](../../modernize/guide.md) ⭐️](#sambercc-skills-golanggolang-modernize-%EF%B8%8F)
- [QA & Performance](#qa--performance)
  - [[golang-benchmark](../../../../go-performance/rules/benchmark/guide.md) 🧠](#sambercc-skills-golanggolang-benchmark-)
  - [[golang-performance](../../../../go-performance/rules/performance/guide.md) 🧠](#sambercc-skills-golanggolang-performance-)
  - [[golang-testing](../../../../go-testing/rules/testing/guide.md) ⭐️ 🧠 ⚙️](#sambercc-skills-golanggolang-testing-%EF%B8%8F--%EF%B8%8F)
  - [[golang-troubleshooting](../../../../go-performance/rules/troubleshooting/guide.md) ⭐️ 🧠](#sambercc-skills-golanggolang-troubleshooting-%EF%B8%8F-)
- [Project Setup](#project-setup)
  - [[golang-cli](../../../../go-cli/rules/cli/guide.md)](#sambercc-skills-golanggolang-cli)
  - [[golang-dependency-management](../../dependency-management/guide.md)](#sambercc-skills-golanggolang-dependency-management)
  - [[golang-pkg-go-dev](../../pkg-go-dev/guide.md)](#sambercc-skills-golanggolang-pkg-go-dev)
  - [[golang-popular-libraries](../../popular-libraries/guide.md)](#sambercc-skills-golanggolang-popular-libraries)
  - [[golang-project-layout](../../project-layout/guide.md)](#sambercc-skills-golanggolang-project-layout)
- [APIs](#apis)
  - [[golang-swagger](../../../../go-web-application/rules/swagger/guide.md)](#sambercc-skills-golanggolang-swagger)
- [Dependency Injection](#dependency-injection)
  - [[golang-dependency-injection](../../../../go-coding-standards/rules/dependency-injection/guide.md) ⚙️](#sambercc-skills-golanggolang-dependency-injection-%EF%B8%8F-1)
  - [[golang-google-wire](../../../../go-libraries/rules/google-wire/guide.md)](#sambercc-skills-golanggolang-google-wire)
  - [[golang-uber-dig](../../../../go-libraries/rules/uber-dig/guide.md)](#sambercc-skills-golanggolang-uber-dig)
  - [[golang-uber-fx](../../../../go-libraries/rules/uber-fx/guide.md)](#sambercc-skills-golanggolang-uber-fx)
  - [[golang-samber-do](../../../../go-libraries/rules/samber-do/guide.md)](#sambercc-skills-golanggolang-samber-do)
- [Frameworks](#frameworks)
  - [[golang-spf13-cobra](../../../../go-cli/rules/spf13-cobra/guide.md)](#sambercc-skills-golanggolang-spf13-cobra)
  - [[golang-spf13-viper](../../../../go-cli/rules/spf13-viper/guide.md)](#sambercc-skills-golanggolang-spf13-viper)
- [samber/\*](#samber)
  - [[golang-samber-do](../../../../go-libraries/rules/samber-do/guide.md)](#sambercc-skills-golanggolang-samber-do-1)
  - [[golang-samber-hot](../../../../go-libraries/rules/samber-hot/guide.md)](#sambercc-skills-golanggolang-samber-hot)
  - [[golang-samber-lo](../../../../go-libraries/rules/samber-lo/guide.md)](#sambercc-skills-golanggolang-samber-lo)
  - [[golang-samber-mo](../../../../go-libraries/rules/samber-mo/guide.md) 🧠](#sambercc-skills-golanggolang-samber-mo-)
  - [[golang-samber-oops](../../../../go-libraries/rules/samber-oops/guide.md)](#sambercc-skills-golanggolang-samber-oops)
  - [[golang-samber-ro](../../../../go-libraries/rules/samber-ro/guide.md) 🧠](#sambercc-skills-golanggolang-samber-ro-)
  - [[golang-samber-slog](../../../../go-libraries/rules/samber-slog/guide.md)](#sambercc-skills-golanggolang-samber-slog)
- [Testing](#testing)
  - [[golang-stretchr-testify](../../../../go-testing/rules/stretchr-testify/guide.md)](#sambercc-skills-golanggolang-stretchr-testify)
  - [[golang-testing](../../../../go-testing/rules/testing/guide.md) ⭐️ 🧠 ⚙️](#sambercc-skills-golanggolang-testing-%EF%B8%8F--%EF%B8%8F-1)

## Code Quality

### [golang-code-style](../../../../go-coding-standards/rules/code-style/guide.md) ⭐️ ⚙️

Golang code formatting, conventions, and project-level style consistency — gofmt, goimports, line length, var declarations, blank lines, comment heuristics.

Use when: the user asks about formatting rules, style review, or project coding standards. Not for naming conventions (→ `golang-naming`), linter configuration (→ `golang-lint`), or doc comments (→ `golang-documentation`).

---

### [golang-documentation](../../../../go-coding-standards/rules/documentation/guide.md) ⭐️ ⚙️

Golang documentation standards — package docs, godoc conventions, example functions, README structure, CHANGELOG, llms.txt, API reference generation.

Use when: writing or reviewing Go doc comments, README files, or API reference. Not for code comments that explain logic (→ `golang-code-style`).

---

### [golang-error-handling](../../../../go-coding-standards/rules/error-handling/guide.md) ⭐️ ⚙️

Golang error handling best practices — error creation, wrapping with fmt.Errorf and errors.Is/As, sentinel errors, custom error types, panic recovery.

Use when: writing or reviewing error propagation, wrapping, logging, or recovery patterns. For samber/oops specifics → `golang-samber-oops`. For preventing panics → `golang-safety`.

---

### [golang-lint](../../lint/guide.md)

Golang linting — golangci-lint configuration, presets, custom rules, CI integration, nolint suppressions, linter selection and output interpretation.

Use when: setting up or tuning golangci-lint, interpreting lint failures, or deciding which linters to enable. For style conventions not enforced by linters → `golang-code-style`.

---

### [golang-naming](../../../../go-coding-standards/rules/naming/guide.md) ⭐️ ⚙️

Golang naming conventions across all identifier types — packages, constructors, structs, interfaces, constants, errors, receivers, acronyms, test functions. Covers MixedCaps rules, Get-prefix, and utils/helpers anti-patterns.

Use when: naming a new type, function, package, or constant. Not for broader formatting (→ `golang-code-style`).

---

### [golang-safety](../../../../go-coding-standards/rules/safety/guide.md) ⭐️

Defensive Golang coding — prevents panics, silent data corruption, and runtime bugs. Nil safety, append aliasing, map concurrent access, float comparison, zero-value design, numeric overflow.

Use when: writing or reviewing code that could silently produce wrong results or panic. Not for external threats (→ `golang-security`) or error handling idioms (→ `golang-error-handling`).

---

### [golang-security](../../../../go-web-application/rules/security/guide.md) ⭐️ 🧠

Golang security best practices — injection prevention (SQL, command, XSS), cryptography, filesystem/network safety, secrets management, cookie security, tool configuration. Audit and review modes.

Use when: auditing a codebase for vulnerabilities, writing security-sensitive code, or reviewing auth/crypto/secrets handling. Not for runtime correctness bugs (→ `golang-safety`).

---

### [golang-structs-interfaces](../../../../go-coding-standards/rules/structs-interfaces/guide.md) ⚙️

Golang struct and interface design — composition, embedding, type assertions, interface segregation, struct tags (JSON/YAML/DB), pointer vs value receivers.

Use when: designing types, choosing between value vs pointer receivers, writing struct tags, or working with interface hierarchies. For architectural patterns that use interfaces → `golang-design-patterns`.

---

## Architecture & Design

### [golang-concurrency](../../../../go-coding-standards/rules/concurrency/guide.md) ⚙️

Golang concurrency patterns — goroutines, channels, sync primitives, context cancellation, worker pools, fan-out/fan-in, pipelines, errgroup.

Use when: writing concurrent code, coordinating goroutines, or reviewing for race conditions. For context propagation specifically → `golang-context`. When cancelling goroutines via context — load both.

---

### [golang-context](../../../../go-coding-standards/rules/context/guide.md) ⚙️

Idiomatic context.Context usage — creation, cancellation, timeouts, values, propagation patterns, WithoutCancel, common anti-patterns.

Use when: propagating deadlines and cancellation signals, or passing request-scoped values. Not for code that merely accepts ctx as first parameter.

---

### [golang-data-structures](../../../../go-coding-standards/rules/data-structures/guide.md) ⭐️

Golang data structures internals and usage — slices (capacity growth, append aliasing), maps, channels, sync primitives, container/\*, generic collections, and when to use each.

Use when: choosing a data structure, understanding slice/map performance characteristics, or using container/list, container/heap, or ring.

---

### [golang-database](../../../../go-web-application/rules/database/guide.md) ⭐️ ⚙️

Golang database access patterns — parameter binding, connection pooling, transactions, migrations, sqlboiler/sqlc code generation, query builders.

Use when: writing SQL queries, designing repository patterns, or configuring database connections. For security aspects of queries (injection) → also consult `golang-security`.

---

### [golang-dependency-injection](../../../../go-coding-standards/rules/dependency-injection/guide.md) ⚙️

Dependency injection patterns in Golang — constructor injection, interface-based DI, wire/dig/fx comparison, and when DI is worth the complexity.

Use when: deciding whether to use DI, designing constructor signatures, or comparing DI libraries. For a specific DI library → `golang-google-wire`, `golang-uber-dig`, `golang-uber-fx`, or `golang-samber-do`.

---

### [golang-design-patterns](../../../../go-coding-standards/rules/design-patterns/guide.md) ⭐️ ⚙️

Idiomatic Golang design patterns — functional options, constructors, builder pattern, middleware chains, circuit breaker, and architecture guides.

Use when: choosing architectural patterns, designing APIs, or implementing resilience patterns. For type-level design (embedding, receivers) → `golang-structs-interfaces`.

---

### [golang-modernize](../../modernize/guide.md) ⭐️

Modernize Golang code using recent language features — range-over-int, min/max builtins, iterators, slices/maps/cmp/slog stdlib packages, testing patterns (t.Context, b.Loop, synctest), and tooling upgrades.

Use when: upgrading a codebase to a newer Go version or replacing pre-generics patterns. Not for lint rule enforcement (→ `golang-lint`).

---

## QA & Performance

### [golang-benchmark](../../../../go-performance/rules/benchmark/guide.md) 🧠

Golang benchmarking, profiling, and performance measurement — pprof, trace, CPU/memory/block profiles, flame graphs, benchstat, CI regression detection, continuous profiling.

Use when: measuring performance, capturing profiles, comparing benchmark runs, or setting up CI regression detection. For applying optimization patterns → `golang-performance`. For debugging a crash → `golang-troubleshooting`.

---

### [golang-performance](../../../../go-performance/rules/performance/guide.md) 🧠

Golang performance optimization — allocation reduction, CPU efficiency, memory layout, GC tuning, pooling, caching, hot-path optimization.

Use when: applying optimization patterns after profiling. Not for measurement methodology (→ `golang-benchmark`) or debugging workflow (→ `golang-troubleshooting`).

---

### [golang-testing](../../../../go-testing/rules/testing/guide.md) ⭐️ 🧠 ⚙️

Production-ready Golang tests — table-driven tests, fuzzing, fixtures, goroutine leak detection (goleak), snapshot testing, code coverage, integration tests, parallel tests.

Use when: writing or reviewing tests. For testify-specific APIs → `golang-stretchr-testify`. For measurement methodology → `golang-benchmark`.

---

### [golang-troubleshooting](../../../../go-performance/rules/troubleshooting/guide.md) ⭐️ 🧠

Systematic Golang debugging — common pitfalls, test-driven debugging, pprof capture, Delve debugger, race detection, GODEBUG tracing, production debugging.

Use when: debugging a panic, unexpected output, or hard-to-reproduce bug. Not for interpreting profiles (→ `golang-benchmark`) or applying optimization patterns (→ `golang-performance`).

---

## Project Setup

### [golang-cli](../../../../go-cli/rules/cli/guide.md)

Golang CLI application development — project layout, exit codes, signal handling, I/O patterns, argument parsing, terminal UX.

Use when: building a CLI tool from scratch. For cobra-specific APIs → `golang-spf13-cobra`. For viper configuration → `golang-spf13-viper`.

---

### [golang-dependency-management](../../dependency-management/guide.md)

Golang module dependency strategies — go.mod conventions, versioning, replace directives, tool dependencies, and multi-module workspaces.

Use when: managing go.mod, dealing with replace directives, or structuring a multi-module repo.

---

### [golang-pkg-go-dev](../../pkg-go-dev/guide.md)

Golang package and module exploration via `godig`, a pkg.go.dev API client (CLI + MCP server) — docs, symbols, versions, importers, licenses, and known vulnerabilities.

Use when: looking up a module's available versions, CVEs, docs/symbols, or who imports it, or searching pkg.go.dev. For upgrading deps → `golang-dependency-management`; for choosing a library → `golang-popular-libraries`.

---

### [golang-popular-libraries](../../popular-libraries/guide.md)

Curated recommendations for production-ready Golang libraries — when the stdlib is enough vs when to reach for a package.

Use when: choosing a library for a new concern (HTTP, logging, testing, etc.). For deep guidance on a specific library → use the library-specific skill.

---

### [golang-project-layout](../../project-layout/guide.md)

Golang project structure and workspace setup — cmd/internal/pkg conventions, monorepo layout, CLI project structure, and when to keep things flat.

Use when: starting a new project or restructuring an existing one. For architectural patterns within the project → `golang-design-patterns`.

---

## APIs

### [golang-swagger](../../../../go-web-application/rules/swagger/guide.md)

OpenAPI/Swagger docs with swaggo/swag — annotation comments, code generation, framework integrations (gin, echo, fiber, chi), security definitions.

Use when: generating OpenAPI documentation from Go code annotations.

---

## Dependency Injection

### [golang-dependency-injection](../../../../go-coding-standards/rules/dependency-injection/guide.md) ⚙️

See "Architecture & Design" section above.

---

### [golang-google-wire](../../../../go-libraries/rules/google-wire/guide.md)

Compile-time dependency injection with google/wire — provider sets, injector generation, wire.Build, and structured DI patterns.

Use when: the codebase imports `github.com/google/wire` or the team has chosen compile-time DI. For runtime DI with reflection → `golang-uber-dig`.

---

### [golang-uber-dig](../../../../go-libraries/rules/uber-dig/guide.md)

Reflection-based DI with uber-go/dig — Provide/Invoke, dig.In/dig.Out, named values, value groups, optional dependencies, Decorate.

Use when: the codebase imports `go.uber.org/dig`. For higher-level lifecycle and modules → `golang-uber-fx`.

---

### [golang-uber-fx](../../../../go-libraries/rules/uber-fx/guide.md)

Application framework with uber-go/fx — fx.New, fx.Provide/Invoke, fx.Module, lifecycle hooks, fx.Annotate, fx.Decorate, signal-aware Run.

Use when: the codebase imports `go.uber.org/fx`. For raw DI without lifecycle → `golang-uber-dig`.

---

### [golang-samber-do](../../../../go-libraries/rules/samber-do/guide.md)

Dependency injection with samber/do — type-safe service containers, lifecycle management, scopes, health checks, graceful shutdown.

Use when: the codebase imports `github.com/samber/do`.

---

## Frameworks

### [golang-spf13-cobra](../../../../go-cli/rules/spf13-cobra/guide.md)

CLI command trees with spf13/cobra — command hierarchy, RunE hooks, flag management, shell completion, usage templates, testing with SetArgs.

Use when: the codebase imports `github.com/spf13/cobra`. For configuration layering → `golang-spf13-viper`. For general CLI architecture → `golang-cli`.

---

### [golang-spf13-viper](../../../../go-cli/rules/spf13-viper/guide.md)

Layered configuration with spf13/viper — flag > env > file > KV > default precedence, BindPFlag, hot reload, test isolation, remote KV integration.

Use when: the codebase imports `github.com/spf13/viper`. For CLI command structure → `golang-spf13-cobra`. For general CLI architecture → `golang-cli`.

---

## samber/\*

### [golang-samber-do](../../../../go-libraries/rules/samber-do/guide.md)

See "Dependency Injection" section above.

---

### [golang-samber-hot](../../../../go-libraries/rules/samber-hot/guide.md)

In-memory caching with samber/hot — 9 eviction algorithms (LRU, LFU, TinyLFU, W-TinyLFU, S3FIFO, ARC, SIEVE), TTL, loaders, sharding, stale-while-revalidate, Prometheus metrics.

Use when: the codebase imports `github.com/samber/hot`.

---

### [golang-samber-lo](../../../../go-libraries/rules/samber-lo/guide.md)

Functional programming helpers with samber/lo — 500+ type-safe generic functions for slices, maps, channels, strings. Immutable (lo), parallel (lop), mutable (lom), iterators (loi), SIMD.

Use when: the codebase imports `github.com/samber/lo`. Not for streaming pipelines (→ `golang-samber-ro`).

---

### [golang-samber-mo](../../../../go-libraries/rules/samber-mo/guide.md) 🧠

Monadic types with samber/mo — Option, Result, Either, Future, IO, Task, State for type-safe nullable values, error handling, and functional composition.

Use when: the codebase imports `github.com/samber/mo`.

---

### [golang-samber-oops](../../../../go-libraries/rules/samber-oops/guide.md)

Structured error handling with samber/oops — error builders, stack traces, error codes, context attributes, public vs developer messages, panic recovery, APM integration.

Use when: the codebase imports `github.com/samber/oops`.

---

### [golang-samber-ro](../../../../go-libraries/rules/samber-ro/guide.md) 🧠

Reactive streams with samber/ro — 150+ type-safe operators, cold/hot observables, 5 subject types, 40+ plugins, automatic backpressure, Go context integration.

Use when: the codebase imports `github.com/samber/ro`. Not for finite slice transforms (→ `golang-samber-lo`).

---

### [golang-samber-slog](../../../../go-libraries/rules/samber-slog/guide.md)

Structured logging pipeline with samber/slog-\* packages — multi-handler routing (slog-multi), sampling, formatting, HTTP middleware, 20+ backend sinks.

Use when: the codebase imports any `github.com/samber/slog-*` package.

---

## Testing

### [golang-stretchr-testify](../../../../go-testing/rules/stretchr-testify/guide.md)

Testing with stretchr/testify — assert, require, mock, and suite packages. Assertions, mock expectations, argument matchers, suite lifecycle, custom matchers.

Use when: the codebase imports `github.com/stretchr/testify`. For test architecture and strategy → `golang-testing`.

---

### [golang-testing](../../../../go-testing/rules/testing/guide.md) ⭐️ 🧠 ⚙️

See "QA & Performance" section above.
