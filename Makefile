##
## EPITECH PROJECT, 2022
## Makefile
## File description:
## build binary
##

SRC		=	game.py

NAME	=	 pbrain-gomoku-ai

all:	$(NAME)

$(NAME):
	@ln -s $(SRC) $(NAME)
	@chmod +x $(NAME)

clean:
	@rm -f *~

fclean:	clean
	@rm -f $(NAME)

re:	fclean all

.PHONY:	all clean fclean re