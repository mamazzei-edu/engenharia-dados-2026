import sys
import subprocess

checks = {
    "Python 3.11+": sys.version_info >= (3, 11),
    "pandas": False,
    "pyarrow": False,
    "boto3": False,
    "jupyter": False,
}

for lib in ["pandas", "pyarrow", "boto3", "jupyter"]:
    try:
        __import__(lib)
        checks[lib] = True
    except ImportError:
        pass

print("=== Verificação do Ambiente ===")
for item, status in checks.items():
    icon = "✅" if status else "❌"
    print(f"  {icon}  {item}")

all_ok = all(checks.values())
print()
if all_ok:
    print("🎉 Ambiente configurado com sucesso! Pronto para a Atividade 2.")
else:
    print("⚠️  Alguns itens precisam de atenção. Revise os passos acima.")
