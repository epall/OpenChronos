#include "project.h"

#ifdef CONFIG_CALTRAIN

#include <string.h>

// driver
#include "caltrain.h"
#include "ports.h"
#include "display.h"
#include "timer.h"
#include "buzzer.h"
#include "user.h"

// logic
#include "menu.h"


// *************************************************************************************************
// Prototypes section
void start_caltrain(void);
void stop_caltrain(void);
void reset_caltrain(void);
void caltrain_tick(void);
void update_caltrain_timer(void);
void mx_caltrain(u8 line);
void sx_caltrain(u8 line);
void display_caltrain(u8 line, u8 update);
extern void set_caltrain(void);

struct caltrain scaltrain;

#endif // CONFIG_CALTRAIN
