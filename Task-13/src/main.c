#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
  while (true) {
    char cwd[512];
    if (getcwd(cwd, sizeof cwd) == NULL)
      break;

    // Gets command
    char input[64];
    printf("%s\n", cwd);
    printf("cshell$> ");
    if (fgets(input, sizeof input, stdin) == NULL)
      break;

    // Splits command and gets the executable name
    char *command = nullptr;
    command = strtok(input, " \n");
    if (command == NULL)
      continue;

    // Loops through and gets the rest of the arguments
    char *args[16];
    int i = 0;
    while (command != NULL && i < 15) {
      args[i] = strdup(command);
      command = strtok(NULL, " \n");

      ++i;
    }
    args[i] = NULL;

    if (strcmp(args[0], "exit") == 0)
      break;
    else if (strcmp(args[0], "pwd") == 0) {
      printf("%s\n", cwd);
      continue;
    } else if (strcmp(args[0], "cd") == 0) {
      if (args[1] == NULL)
        continue;
      if (chdir(args[1]) != 0)
        break;

      continue;
    } else if (strcmp(args[0], "echo") == 0) {
      int length = 1;
      int i = 1;
      while (args[i] != NULL) {
        length += strlen(args[i]);
        ++i;
      }

      char *final_result = malloc(length * sizeof(char));
      final_result[0] = '\0';

      // Builds the final string from array
      i = 1;
      while (args[i] != NULL) {
        strcat(final_result, args[i]);
        ++i;
      }

      printf("%s\n", final_result);

      free(final_result);
    }

    // Makes a new process and transforms it to the intended program
    pid_t pid = fork();
    if (pid < 0)
      break;
    else if (pid == 0) {
      execvp(args[0], args);
      exit(EXIT_FAILURE);
    } else
      waitpid(pid, NULL, 0);

    i = 0;
    while (args[i] != NULL) {
      free(args[i]);
      ++i;
    }
    continue;
  }

  return 0;
}
