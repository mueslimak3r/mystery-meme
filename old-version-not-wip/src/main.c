#include "steg.h"
#include <unistd.h>

void	parse_source_file(unsigned char *data_ptr)
{
	uint64_t png_header = (uint64_t)*data_ptr;
}

long	validate_input_file(char *filename)
{
	struct stat buf;

	if (stat(filename, &buf) == -1)
	{
		perror("error: ");
		return (-1);
	}
	return (buf.st_size);
}

int		main(int ac, char **av)
{
	long filesize;

	if (ac != 2)
	{
		printf("error: no input given\n");
		return (1);
	}

	filesize = validate_input_file(av[1]);
	if (filesize < 1)
		return (1);

	int source_fd = open(av[1], O_RDONLY);
	if (source_fd < 1)
		return (1);

	unsigned char *source_file = (unsigned char *)mmap (0, filesize, PROT_READ, MAP_PRIVATE, source_fd, 0);


	int dest_fd = open("new", O_WRONLY | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
	write(dest_fd, source_file, filesize);

	parse_source_file(source_file);

	close(dest_fd);
	munmap(source_file, filesize);
	close(source_fd);
	return (0);
}