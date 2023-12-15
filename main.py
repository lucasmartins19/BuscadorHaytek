import login
import requests
import PySimpleGUI as sg
from concurrent.futures import ThreadPoolExecutor
import threading
import locale

def main():
    empresas = usuario.verificar_empresas()
    dados = list()
    empresas = [f"{empresa}: {empresas[empresa]['Nome']}" for empresa in empresas]
    usuario.codigo_empresa = empresas[0].split(":")[0]
    ring_gray_segments_big = b'R0lGODlhQABAAKUAACQmJJyenNTS1GRmZOzq7Ly+vDw+PNze3ISGhPT29MzKzDw6PLS2tExKTCwuLKyqrNza3GxubPTy9MTGxOTm5IyOjPz+/CwqLKSipNTW1GxqbOzu7MTCxERCROTi5Pz6/MzOzExOTJSSlP7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQJCQAjACwAAAAAQABAAAAG/sCRcEgsGouWxIYwlDw4B8txSq1ahx8CRMEpcBTDA2B8CSEKkqt6LbQQMl2vHCwUAy7ke6TwYfuRHhNdg3IcE0MeY3eKeBcGGAl/bBaBhJZeh0KJeIqddwsYUpJVEgqFp4R0I3aerQAhAqNTHqi1XaoHnK6MdwGyRB8Ctra4no2LnXgaG78jHyCX0XNhuq7VYyFpv8/Dl8W8x7sio31Y0N3TddfgyAAV5AoHwCDot2Hs63jjWOVXwlDzpHWZIMDDkA0IBizY1WmfkFKxrtAaJM8cqgkHIlERIKKDOCISBHDgYJDUpZJCng1SQEDUlQ8MGnh614SLHG1HLNA7SSQB/jQPLtl8wHBBH0iRXrqACEqEgsCKKXGOgtCA5kNhhbpQOPJB0DCUzZoAs2lpZD9E9aCGLRJMYAGwIyx4dauA6VpubicEJVCPg8a1IEd248BkyL9uagGjFSwtojO3Su0qtmAKcjm+kAsrNoLZVpfCENDV3cy18jAIQkxLS0w6zCBpYCxA5iC1dZN6HySgy2TbyFxbEghAdtybyGFpBJx2Q128yAHIW5tLn069uvXrQ5QLZE79eTcKnRtbP16LgATIvKf/jibBQr3avXVbHqG6Ftze3gXSCU1X8uYP9V3CXHi2aNYbgdEU9gFkBYzWG2W4GVbPfYpN1A1xCKLil20J7zDIQXRtrFeLg//tNIxeRVj4VG8qeXZfV26x1kxQeGl4VnYrYvHXKKWo1aIlICJBViE+/uRfFZRQNM8pS1EhH5EBecHSkUgQUB9YP9JmhYpFEoKJB/CBdECAXhRZphr/mCkQQSglcIAAE6Q1D3FVPNMlOg0O0WE9cmB5Y51LeqjKkx6+ddc5gt5WqJLbmJioEAnwaYkCfwpFnlsFgKCopAUIUOkfKg42KKckbVYKn6pEKigzpFlAgYiTbromBVQ280EltWTaBF0efNoqAUi9putDtmTQEnbOaGGipg8RAgIEBPh6XRJL6EnBBgnUykYQACH5BAkJACQALAAAAABAAEAAhSQmJJyanMzOzGxqbOzq7LS2tERCRNze3PT29MTCxDw6PKSmpNTW1IyKjExOTCwuLPTy9Ly+vOTm5Pz+/MzKzFRWVCwqLJyenNTS1Hx+fOzu7Ly6vOTi5Pz6/MTGxDw+PKyqrNza3JSSlFRSVP7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb+QJJwSCwaixOEhjDsSDSIyXFKrVqbhBAlEUlQhogulxIidK7otHBCYHC78K8Qwa3DGQSpek+ccDx2gR5gcIFdHhJnfGl+gIWPCYNzhoGRHHqLVBAUkJ1yJHSdhhQQmVMcop5glKIJHKZEHRiplJ8QtI9dGIqmHQKsrJ+hwJ0CvJm+uHbCypAHyLG/zcLElM+LHRTXQsnVEczeddskEKVoswnjvsQeGK9zIRiOxOMQFQNoqOLRkB4HCFUgHOBkjYg9AAAuWIFg6B03aV7yMCJAEE69ChYAWLDAgMoEAZ0cgvp1aZGffUPsZUQIYASmIhKAqTNnatPFlQgzLjjSYV7+SFhHXh5kSVQBwCL6aI0DWuQgTqIAAiDxGewlUyFOobK0oOAYAWUJjl4lcuDBU41oEW4ggk7p2CMXtGrFx82bAKtvSXRwsBUtTgvmvlZjktdIAblpAawlEQIXBbyFOxjImXhlBiEVWS0tPETE07MOSEyoloAmZyIh+hLNaKHDLXanpyhAzBIDgWoYYh8ZoLrvhpi0Qug20oC2RhDDkytfzry5cyLAgQlnfqCaBMGpcjNvy4oAQ1qSllOFBGGCMtO6X9M6k/mn8uq05DQm9jh5NlzTsQMjrFu/KMIdeFNfbBO0Rwkv3IkiUmFJAaOdEP5REtZpw9AiQR/jjQIZUN3bpOKBVQ2KstlY67SyoF4ZWlTYSx1WcswQ0TkTi1iZ2BQNJRcGtYWMTZC0YRUndaEOSHbcpQmPD9VBgURosNGeSCUmUJoVDQ5pxyEcoNfUQCLyk845QnopSjsOIXCAPMoM+aAVvliJyzerNMMFlC9WcUyL8aUkJxwnYgORMrbsiVIvRMoJjqAU1KmGLHtGIICe4cCxy1UhAuMFpHL2WZOBqsxhqAacTSBBikpiCgwiPzLVwR+sOJoSfRwoGioBGFTiKlai4JFqbB1kUeijWBVZhqzPJbEEGE9E8VYQACH5BAkJACQALAAAAABAAEAAhSQmJJyanMzOzGRmZOzq7LS2tDw+PNze3PT29MTCxHx+fDQyNKSmpNTW1ExOTPTy9Ly+vOTm5Pz+/MzKzIyKjCwqLJyenNTS1GxqbOzu7Ly6vERCROTi5Pz6/MTGxDw6PKyqrNza3FRSVJSSlP7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb+QJJwSCwaixJEhjDsRDIIyXFKrVqbhNAkAUlMhogudxIidK7otFBCaHC78K8Qwa3DGwSpek+UcDx2gR5gcIFdHhFnfGl+gIWPCYNzhoGRHHqLVA8TkJ1yJHSdhhMPmVMcop5glKIJHKZEHReplJ8PtI9dF4qmHQKsrJ+hwJ0CvJm+uHbCypAHyLG/zcLElM+LHRPXQsnVEMzeddskHcdVswnjvsQeF69zIReOxOoCF2io4tGQHgcIVQ8OcLIWjcs7TYYOkpPmJQ8jAgPh1KuToNQUCQI6KUTw69IiP/qaMIQAQQCmIhGAqbNoatPEQlwiHOkwTyOsIyfXdfJgjkT+PlrjbhbpJkohCQk1g50Uym0kJQ8nCShL8I9pkQfhmAxBB9TqkQjK7nHzZtKrEQlbcCmSWk2rWZTetIbANWHp26MRWYUQkrdT0LtCfgY7Wq0iYCO3qklInErS4SJJIT0gUE3sYyJcWRFISWvvZSIHqsn8TLq06dOoS3MG5rk0BQCwY8sGAIJtKsukMQCosLs3b94QsNJyTPrD7OMhJChjebkBbN7Hd//rm7D0iOiyHQiZS6zu5w4besuGDkCBENvA3B7WcBz67wJj6dr12sHBc+wVWGYu+tjC/di/7TYAEei1UtVbByyAnWwa9BHZKPPd9IAI4t332wfmCCbKX1bfTbggAAEYQRM9b53koYW7LcDcEKs5E8uBmbhExImzgXBRWoFM5BEfIHUxjocBitDTEIyF1FQdEziEBht9KURjBbgdIdhLb1iy4lUCbTgjhSCigU49w7kDxgHyKPOjCAOi4QuVqXyzSjMGzXglFccQVY0tcMJhFDJO0YJnOIVwqIadyoCTpxdDpiFLniUReSgEuzClITBeOAqoK2ZtMg0h4UyQwV0SRPBgIX8OF0GETHXwByuNCiFcMBwkWiIBF1TSKglFFoIHqo91kEVGXAhApB0ClCErakksAcYTUXgVBAAh+QQJCQAhACwAAAAAQABAAIUkJiScmpzMzsxkZmTs6uw8Pjy8urzc3tz09vSEgoQ8OjzU1tRMSkzExsQsLiykoqT08vTk5uT8/vyUkpQsKizU0tRsbmzs7uxERkTEwsTk4uT8+vyMiozc2txMTkzMysykpqT+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/sCQcEgsGosSxIUw3EQuCMlxSq1am4TOJ2PIfIaILlfQIWyu6LRQQlhk3uJMA8x92zMVglTNJ0o0DXVxXXNCCHZdiW8NEWd9aX+BcYKBhSGHYgaBdVyMe49UEFuDnZqEdIJcpogCEKBTGpycpg2mAmCZtQ26pBqvRBsVd7m0mnKoxcWdXAuOrxsCipTFusi816uLn6DQcNTUlpjY42IH3EQIAqXkldbf2OaPGx/xQt3vq+Fw7LT1IRLOrAjL4C+dpHENBNTbsGDBQXz+JAiogCZWOWDqiilEUAXBgV3fIqDLKLIKhGEER3YSEGFbFQkRMuqKqM7OBSoSpXGh2eCA/ks0MGeqVCTgp5AIiAwYSwmG4y8EPf3UzFayyIZadni98fdryLZ0+/IFFBJrGtYuXLtiNHvRD9Z1tOQY7dotrNYG2wggYudUbZGTs7BlqBqiQiJ2af0KOWCX2i17e78VVXxEItxrGZwiPfztJuUjm8m9KdmhMa/Jn41IACl6gZBRiFNPYXzZ1j9i2PrKRodvkwTAvXdPeSh4SW1dj4UXcYMvwwWkx5kqJ+LwuAHC07Nr3869u/fNcMLv7M44k/jresPupch9YKm9BE5OkmVJ+1uUby5IMM85//Yw3kyTgRQyfSPddLTh85gb0eGVnQQf4EaLayEQwJlWXWAnW3rR/pW0gWm0fDCXXxCyVYsmfQlAnDKJKRaBhLokRIRevb2hG2WHgIgVYatZN8aIz0RjnYNEJBjbbmAdp2GPEKWmm2XvGAVdSOjc2McBDEww1DUarrFJMTRloAGQU2zwgAMAAKAlGCp2ktCI4phCWJIGCKAHJAYwkCYAFKi5pQFWFvFRJwVNBQc9rlDRwQQY7NnnnmsaQhIaNYWJyDANVOCLEARwMIACe/LpqKiRXiIAhVdAU6g3WrEyxAKhihprqKVuMFZHUpmoVFZDdCDqo7OGSkGpQUaGmVK79BrssmkOS1dGQxpjia/L9mltqAwkys1AveWjLLCyztrnANr+YmS3VcnBKu6vvwbw2QUFsjNtuOBiy95nQQ05b6zX8qnAA+U6GQFr4HzbbKwKBBCwcBJcwNw1+wpLwQAGLKxdwwdE044QvlrLQAIVe4eTElVdAEIGHdz6ShAAIfkECQkAIQAsAAAAAEAAQACFJCYknJqczM7M7OrsZGZkREJEtLa03N7c9Pb0xMLEPDo81NbUhIKELC4s9PL0TE5MvL685Obk/P78zMrMLCospKKk1NLU7O7sbG5svLq85OLk/Pr8xMbEPD483NrclJKUVFZU/v7+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABv7AkHBILBqLEsRlMNxELgjJcUqtWpsDzyQBSUyGiC534hlsrui0UDJYcLvwrxDBrcMXA6l6T5RoOHaBHGBwgV0cEWd8aX6AhY8Jg3OGgZEaeotUDhOQnXIhdJ2GEw6ZUxqinmCUogkapkQbFqmUnw60j10WiqYbAqysn6HAnQK8mb64dsLKkAfIsb/NwsSUz4sbE9dCydUQzN512yEbx1WzCeO+xBwWr3MeFo7E6gIWaKji0ZAcBwhVDg5wshaNyztNhg6Sk+YlD6MBA+HUq5Og1BQJAjopRPDr0iI/+powhABBAKYiEYCps2hq08RCXCIc2TBPI6wjJ9d14mAuRP4+WuNuFukmSmEICTWDnRTKbSQlDicHKEvwj2kRB+GYDEEH1OqRCMrucfNm0qsRCVtwKZJaTatZlN60esA1YenboxFZeRCSt1PQu0J+BjtarSJgI7eqSUicStLhIkkhORhQTexjIlxZDUhJa+9lIgeqyfxMurTp06hLcwbmuXRoWhHYprJMOnOnAVhpOSYdOZADCcpYXmYM7EzfhK6ryZlLrO7nbLg8ywbm9vB0UVo3eHN+GK0yXrYpGTUrWBTt65SoAh4Gu0/vR9zNEmUFtUh5goB1ph9Pk97bnBml11MIqzlDREA3uVQQJKOdlVYg4zgAQgMVDGgFSF3U80hZU+QQl+GBIFAAAAAPZGDhWRA9opB+hlUhWIQgjAiAiAAU8EFrRwTEiU1gSDPeEejAKCKNMo6oAAEBNBEPB8rUQ1sVvsBYZJE0ivjAELc0Y1AsJxpxjIQzTikmiViGU8hfi4BJ5JgyXilEbmZuCYuaUw45IpFuhgCnliV1aYUDBLB5p4xWlslnArswFQAFRNo56Ih57unNj6ZY8MCYjZL5ppkCCGfVBhUoEGamkBrKTiKPORAqmxQUYKonGvj5aQYYMEqlq9yIgoddpDmQAQMPDIkrOYWQYUZqU2zgQQIGNKHBAFF4FQQAIfkECQkAJgAsAAAAAEAAQACFJCYknJqczM7MZGZk7OrstLa0PD483N7cfH589Pb0xMLETEpMNDI0pKak1NbUjIqM9PL0vL685Obk/P78zMrMVFJUlJKULCosnJ6c1NLUbGps7O7svLq8REJE5OLk/Pr8xMbETE5MPDo8rKqs3NrcjI6M/v7+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABv5Ak3BILBqLk8SGMPxINonJcUqtWpsEEkURUVCGiS6XQiJ8rui0cEJwcLvwrzDBrcMdBKl6T5x4QHaBIGBwgV0gEmd8aX6AhY8Kg3OGgZEeeotUEBSQnXImdJ2GFBCZUx6inmCUogoepkQfGamUnxC0j10ZiqYfAqysn6HAnQK8mb64dsLKkAfIsb/NwsSUz4sfFNdCydURzN512yYfx1WzCuO+xCAZr3MkGY7E6gIZaKji0ZAgBwlVEA5wshaNyztNhg6Sk+YlDyMCA+HUq6Og1JQJAjopTPDr0iI/+powjBBBAKYiEoCps2hq08RCXCQc+TBPI6wjJ9d1AmHORP4+WuNuFukmSqGJCTWDnRTKbSQlECcJKFPwj2kRCOGYDEEH1OoRCcrucfNm0quRCVtwKZJaTatZlN60ksBFYenboxFZkRCSt1PQu0J+BjtarSJgI7eqTUicStLhIkkhQSBQTexjIlxZEUhJa+9lIgeqyfxMurTp06hLjwDAurVrAA9Oh6YFFsAF27hv39ZwOnOnLK+DizgdORCEBLeDt77goDRjYGdCJFcOwEJpwapMIHidPHkHu2+z4fJcYDnr6aw5fGZLSysE9OZZLwBvVXw1XgO6495/IcBjD95YZgIH1O3HgGdvDdNeLCKcl9trC/QklE7AQFVEAAXiFhtgFOradFWD+722oVfHdGgHT0es5qBrI5LDUiYuFQTJaEZ8UIFy1g0BQQau0FcFSAYRwVEgdVGRgW6ttbgjB2M4hAYbaYXUlB0vHoGhhrFsocAyB1R5lUCi1NOFUVMMwFqL2WzJJD/ugHGAPN4o5IuAAC2QoxA7KsAkMdQ0EyQYEk7xYppb0qWjn3CQiQ2PXawJjC2ISolMRuF0AU6kFASKhiyVjnFopxHswhR2xAigI6iKttTXYHj6ScpdjVRzaYUeHfbBH49+KgoIHmhqFhuMEkkIJRk4idoHWaRV0qlikGFGahcp4VYCT0ThVRAAIfkECQkAJAAsAAAAAEAAQACFJCYknJqczM7MbGps7OrstLa0PD483N7c9Pb0xMLETEpMPDo8pKak1NbUjIqMLC4s9PL0vL685Obk/P78zMrMVFJULCosnJ6c1NLUfH587O7svLq8REJE5OLk/Pr8xMbETE5MrKqs3NrclJKU/v7+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABv5AknBILBqLE4SGMPRINIjJcUqtWpsEESURSVCGiC6XIiJ4rui0cEJocLvwrxDBrcMbBKl6T5x0PnaBH2BwgV0fEmd8aX6AhY8Jg3OGgZEdeotUEBSQnXIkdJ2GFBCZUx2inmCUogkdpkQeGKmUnxC0j10YiqYeAqysn6HAnQK8mb64dsLKkAeZpU2/zcLElM+LECAjsQLUhNaF2EIex1UDAADc0sQfGK9zIhiOxOMkvhhoF+np6+Tegg4gqALhAKdr3bjAo9LAAgCHDv3dm+YlDyMCB+HY81UnQbQjEyrwGymR4wFMavzU2UgxQgQBKIkwgMjPobpYA2FtYlkpgv6EIwgWjBwZERbIhJ0+mCMRYKhTCxKNFkHQspK9ewYeEh2qIKdUpMA+oCxgs6ZZCyK+GhlG6+cQdE61pgug9kiHcPmEaHiwtawFBUvrTthCK4EisnHlFqg7hQCuCExIZOhbc0FgxoNxpSUBIm7ZqIyJiLD2xYNfueks5A1tBEK4CQ1QO13AmkoCa7co8xtQewoGawRCJE7toPeR0W2NK1/OvLnz51YkWNvc/IA1CY6JrWY+ixgB17QkNacnCsIEZR+V37J2JiOrhcqt05IjAheFmKw9uO+0OTutyMb5B0xkHoRzn3GZsTdEd7TAFxoq1mwnYCteMcYWMG6tQV4w+N9JlUw7MUFIy1V1cdSKg/ds+AiJRqH0ISSGHSGdKBtVmA0FPEGSIRKEBcLTJYuo1AVLj8CkiTNgUWARGmzsB5+Jt6VnlzhguWSJlEUUtN9K3QyJRndEhvUOGAfMowxL21XhS47ERFBNMwrFctkRx7xI2hDrwRkBiotAqYwtenIJi51/ghMoBXNeIYueL+EZaAS7fCWiNV44Gk4dfJqyyTdzwEmBBqxNIIGKgQBqDSIdquXBH6w0KgR4wXSQqGAE/FYIFwJYCgkeqSrnQRYAuUoCrC+VMatzSSwBxhNR1BUEACH5BAkJACQALAAAAABAAEAAhSQmJJSWlMzOzGRmZOzq7Dw+PLS2tNze3PT29ExKTISGhMTCxDw6PNTW1CwuLJyenGxubPTy9ERGROTm5Pz+/FRSVMzKzCwqLNTS1GxqbOzu7ERCRLy+vOTi5Pz6/ExOTJSSlMTGxNza3KSipP7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb+QJJwSCwai5TDwjD0TDQIynFKrVqHEY7icwFcJEPEgrNYWEQEz3XNFno4EIcXMAcLI+MxmdwgSNuARAgjBXN0hwB2JGJ7eXsWHX+BaxQjDIZdiAAJWI6eHGQhE5KTUxgfmql0nHeNrp4WEaVTD122qpmsJHivvWQds0QRA5mqhqtYvZ9lZBhqwREVdMWHxZkbTcraHALPs9Gp1tMA2EKMy8oLB6XeuxXU45rlJG/o6OuTHhb4d9Lxc7fm8bLnih+9dlUwkDEYTRwiBgNANBGBgRlBYE0EYFjToRFDf+MYgNhIJUKHEPeIeBAwBmPJTy7dzUlgACEVDwQsuIq5spH+rCkUBPSK2fDBT0AUOjAzuNKTAFJEJthjKCLYrn0qWb6acMQDSm0xrbrJii6EzY4E1Ymd0hQskq8ELUBd29ZeCFIEtOVZgGCtkYF6CRBRmNag3yET9IIiSS8tt7mHKei0N+ZZ3rSCDx+5HFiICMVyNR+RrLgqicnaDIseokSvBRIU0i44ulqY4gUeshAMUXsKXF8ICKRl3Huw3gUEpOo1XZxIa3QcuDafTr269evYEadlTv25sgmc0RGfTlgbAcDLeFv/vSwChdu0i+vWqwY1urC9vS97TeJzXMia6VOaEOEpk1lxBS6TmQeOhdYbaWl5U549+B2Gll7EJfgKX7XznaOXdEJQwF4vDgYo1G5QXThVb3VtiJ9XBKlmFSk9LYPbEcotw1Rf0GCV0TIgImGBjmRFMklSeTB14h5PlfSKknlY4AcbFOS0E1lkzGaFilDuEUoH8RURwQH2eZTVQmsQpqReIWDgEgIHYBDCbUqOd5MAXRLEAX+LOOYITzbddKaffM7nJwcVBtJiWoXe9qRVNTpqRhiSNmJBoGx4MKFi3CRz6BjOrKXicY1+mmgpEZSJDp8ISGqBBqtRMMGIsHjK5ijFeXASdAJ0og0kmIpWZUWNjNFrK8v0AWBzOImw5LG7OCIAGsFiRwECGhyIwBNRHBYEADtyVDFRVDhwUWtrU3FYaml4RUhlL3B5anRyd0U0elhCZEd5WG9UUEc3UXFBQnpBa3NVdUk0UkI2T2tXS0xKdlBD'
    
    layout_principal = [
        [sg.Text("Empresa:"), sg.Combo(values=empresas, default_value=empresas[0], key="empresa", enable_events=True, readonly=True, size=(30))],
        [sg.Input(size=(20), key="campo_pesquisa", readonly=True), sg.Button("Pesquisar", key="pesquisar", disabled=True)],
        [sg.Table([], key="tabela", row_height=20, headings = ["Lente", "Nome", "OS","OD ESF.", "OD CIL", "OE ESF", "OE CIL", "AD OD", "AD OE", "PEDIDO", "VALOR"])],
        [sg.Image(data=ring_gray_segments_big, pad=0, key="animacao_dados", visible=True)],
        [sg.Push(), sg.Text("0", key="Registros", pad=0)]
    ]
    window_principal = sg.Window("BuscadorHayTek", layout=layout_principal, finalize=True)

    threading.Thread(target=lambda: usuario.extrair_dados_pedidos(window_principal), daemon=True).start()
    master = window_principal['animacao_dados'].widget.master
    master.place(in_=window_principal['tabela'].widget, anchor="center", relx=0.5, rely=0.5, bordermode=sg.tk.OUTSIDE)

    while True:
        event, values = window_principal.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "empresa":
            usuario.codigo_empresa = values['empresa'].split(":")[0]
        elif event == "pesquisar":
            if values['campo_pesquisa'] == "":
                window_principal['tabela'].update(values=usuario.pedidos_l_org)
                window_principal['Registros'].update(value=len(usuario.pedidos_l_org))
            else:
                resultados_filtrados = usuario.filtrar_resultados(values['campo_pesquisa'])
                window_principal['tabela'].update(values=resultados_filtrados)
                window_principal['Registros'].update(value=len(resultados_filtrados))

        elif event == "carregando":
            dados.append(values['carregando'])

            window_principal['tabela'].update(values=dados)
            window_principal['Registros'].update(value=len(dados))

        elif event == "carregou":
            window_principal['campo_pesquisa'].update(readonly=False)
            window_principal['pesquisar'].update(disabled=False)
            window_principal['tabela'].update(values=usuario.pedidos_l_org)
            window_principal['Registros'].update(value=len(usuario.pedidos_l_org))
            master.place(in_=window_principal['tabela'].widget, anchor="center", relx=2, rely=2, bordermode=sg.tk.OUTSIDE)

        window_principal['animacao_dados'].update_animation(ring_gray_segments_big, time_between_frames=100)

    window_principal.close()

class Usuario:
    def __init__(self, dados_login):
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Token": dados_login['TOKEN'],
        "Iduser": str(dados_login['ID'])}

    def requisicoes_get(self, url):
        try:
            return requests.get(url, headers=self.headers)
        except:
            return None

    def filtrar_resultados(self, termo):
        return [lista for lista in self.pedidos_l_org for item in lista if termo.lower() in item.lower()]
        
    def verificar_empresas(self):
        requisicao = self.requisicoes_get("https://api.haytek.com.br/api/v1/user/legacy/users/24342/config")
        if requisicao is not None:
            empresas = requisicao.json()['RESULT']['COMPANIES']
            empresas_dict = dict()
            for empresa in empresas:
                empresas_dict[empresa['A1_COD']] = {}
                empresas_dict[empresa['A1_COD']]['Nome'] = empresa['A1_NOME']
            return empresas_dict
        return None
    
    def funcao_auxiliar_requisicao(self, pedido):
        try:
            requisicao = self.requisicoes_get(f"https://api.haytek.com.br/v1.1/orders/{pedido}/details/PARAPAR").json()['RESULT']['PARAPAR']
            if len(requisicao) > 1:
                for req in requisicao:
                    self.pedidos_l.append(req)
                    self.window_principal.write_event_value("carregando", [req['DESCRICAO'].strip("Lente Haytek Visão Simples Acabada"), req['NOME'], req['OSCLI'], req['DIR_ESFER'], req['DIR_CIL'], req['ESQ_ESFER'], req['ESQ_CIL'], req['DIR_ADD'], req['ESQ_ADD'], req['PEDIDO'], locale.currency(req['VALOR'], grouping=True)])
            else:
                self.pedidos_l.append(requisicao[0])
                self.window_principal.write_event_value("carregando", [requisicao[0]['DESCRICAO'].strip("Lente Haytek Visão Simples Acabada"), requisicao[0]['NOME'], requisicao[0]['OSCLI'], requisicao[0]['DIR_ESFER'], requisicao[0]['DIR_CIL'], requisicao[0]['ESQ_ESFER'], requisicao[0]['ESQ_CIL'], requisicao[0]['DIR_ADD'], requisicao[0]['ESQ_ADD'], requisicao[0]['PEDIDO'], locale.currency(requisicao[0]['VALOR'], grouping=True)])
        except:
            return self.funcao_auxiliar_requisicao(pedido)

    def extrair_dados_pedidos(self, window_principal):
        self.window_principal = window_principal
        pedidos = self.lista_pedidos()
        if pedidos is not None:
            self.pedidos_l = list()
            with ThreadPoolExecutor(max_workers=10) as pool:
                pool.map(self.funcao_auxiliar_requisicao, pedidos)
            self.pedidos_l_org = sorted([[pedido['DESCRICAO'].strip("Lente Haytek Visão Simples Acabada"), pedido['NOME'], pedido['OSCLI'], pedido['DIR_ESFER'], pedido['DIR_CIL'], pedido['ESQ_ESFER'], pedido['ESQ_CIL'], pedido['DIR_ADD'], pedido['ESQ_ADD'], pedido['PEDIDO'], locale.currency(pedido['VALOR'], grouping=True)] for pedido in self.pedidos_l], reverse=True, key=lambda l: int(l[9].strip("MG")))
            self.window_principal.write_event_value("carregou", '')

    def lista_pedidos(self):
        try:
            json = {
                "id_ini": 0,
                "id_qtd": 0,
                "status": "T",
                "data_ini": "19000101",
                "data_fim": "21000101",
                "companies": [self.codigo_empresa]
            }
            pedidos = requests.post(f"https://api.haytek.com.br/v1.1/orders/history/v2/{self.codigo_empresa}", headers=self.headers, json=json).json()['RESULT']
            return [pedido['Pedhtk'] for pedido in pedidos]
        except:
            return None

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    dados_login = login.iniciar_login()
    if dados_login is not None:
        usuario = Usuario(dados_login)
        main()