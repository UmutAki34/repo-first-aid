# Repo First Aid

Practical, dependency-free checks that help a GitHub repository become easier to run and easier to contribute to.

Türkçe: Bir GitHub projesini çalıştırmayı ve projeye katkı vermeyi kolaylaştıran, bağımlılıksız ve pratik kontroller.

## Installation / Kurulum

Clone the repository and run it directly with Python.

Türkçe: Depoyu klonlayıp Python ile doğrudan çalıştırabilirsin.

```bash
python -m repo_first_aid /path/to/repository
```

For machine-readable output / Makine tarafından okunabilir çıktı:

```bash
python -m repo_first_aid /path/to/repository --json
```

## What it checks / Kontroller

- README with installation, usage and test guidance / Kurulum, kullanım ve test bilgisi içeren README
- Project metadata such as `pyproject.toml` or `package.json` / `pyproject.toml` veya `package.json` gibi proje metadata dosyaları
- CONTRIBUTING and CODE_OF_CONDUCT files / Katkı rehberi ve davranış kuralları
- License and `.gitignore` / Lisans ve `.gitignore`
- `.env.example`-style environment documentation / `.env.example` benzeri ortam değişkeni dokümantasyonu
- Common secret-file patterns / Yaygın secret dosyası kalıpları
- GitHub Actions workflows / GitHub Actions iş akışları

The first release prefers clear, actionable advice over a large number of noisy checks.

Türkçe: İlk sürüm, çok sayıda gürültülü kontrol yerine açık ve uygulanabilir önerilere öncelik verir.

## Tests / Testler

```bash
python -m unittest discover -s tests -v
```

## Contributing / Katkı

Small improvements are welcome. Please add a focused test for behavior changes and keep the CLI dependency-free.

Türkçe: Küçük iyileştirmeler memnuniyetle karşılanır. Davranış değişiklikleri için odaklı test ekle ve CLI'yi bağımlılıksız tut.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details / Ayrıntılar için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bak.

## License / Lisans

MIT. See [LICENSE](LICENSE) / MIT. [LICENSE](LICENSE) dosyasına bak.

